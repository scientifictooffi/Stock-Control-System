from datetime import date as _date

from stock_control.models import Batch, Movement
from stock_control.storage import StockStore

LOCATIONS = {"MAIN", "BACKROOM", "SHOPFLOOR", "QUARANTINE"}
ADJUST_REASONS = {"COUNT", "DAMAGE", "THEFT", "FOUND"}
RETURN_CONDITIONS = {"NEW", "OPENED", "DAMAGED"}
MAX_RECEIVE_QTY = 10000
RETURN_WINDOW_DAYS = 30
CRITICAL_DAYS = 7
NO_EXPIRY = "9999-12-31"


def _record(store: StockStore, sku: str, movement_type: str, quantity: int,
            date: str, reference: str = "") -> Movement:
    movement = Movement(store.next_id("MV", store.movements), sku,
                        movement_type, quantity, date, reference)
    store.movements.append(movement)
    return movement


def _fifo_key(batch: Batch):
    return (batch.expiry_date or NO_EXPIRY, batch.received_date)


def _unique_batch_id(product, base: str) -> str:
    existing = {b.batch_id for b in product.batches}
    candidate, n = base, 1
    while candidate in existing:
        n += 1
        candidate = f"{base}-{n}"
    return candidate


def _take_fifo(product, batches: list, quantity: int) -> list:
    taken = []
    remaining = quantity
    for batch in sorted(batches, key=_fifo_key):
        if remaining == 0:
            break
        qty = min(batch.quantity, remaining)
        batch.quantity -= qty
        remaining -= qty
        taken.append((batch.batch_id, qty))
    product.batches = [b for b in product.batches if b.quantity > 0]
    return taken


def receive_stock(store: StockStore, sku: str, quantity: int, batch_id: str,
                  received_date: str, expiry_date: str = None,
                  location: str = "MAIN"):
    product = store.get_product(sku)
    if product.status == "DISCONTINUED":
        raise ValueError("cannot receive a discontinued product")
    if quantity <= 0 or quantity > MAX_RECEIVE_QTY:
        raise ValueError("quantity must be between 1 and 10000")
    if location not in LOCATIONS:
        raise ValueError(f"unknown location: {location}")
    if any(b.batch_id == batch_id for b in product.batches):
        raise ValueError(f"batch {batch_id} already exists for {sku}")
    if expiry_date is not None and expiry_date <= received_date:
        raise ValueError("expiry date must be after the received date")

    product.batches.append(Batch(batch_id, quantity, received_date, expiry_date, location))
    _record(store, sku, "RECEIVE", quantity, received_date, batch_id)
    return product.on_hand


def issue_stock(store: StockStore, sku: str, quantity: int, date: str) -> list:
    product = store.get_product(sku)
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    issuable = [b for b in product.batches
                if b.location != "QUARANTINE"
                and not (b.expiry_date is not None and b.expiry_date < date)]
    issuable_units = sum(b.quantity for b in issuable)
    if quantity > product.available or quantity > issuable_units:
        raise ValueError("not enough stock available to issue")

    taken = _take_fifo(product, issuable, quantity)
    _record(store, sku, "ISSUE", quantity, date,
            ",".join(batch_id for batch_id, _ in taken))
    return taken


def adjust_stock(store: StockStore, sku: str, counted_qty: int, reason: str,
                 date: str) -> int:
    product = store.get_product(sku)
    if counted_qty < 0:
        raise ValueError("counted quantity cannot be negative")
    if reason not in ADJUST_REASONS:
        raise ValueError(f"unknown reason: {reason}")
    if counted_qty < product.reserved:
        raise ValueError("counted quantity is below reserved stock")

    on_hand = product.on_hand
    difference = counted_qty - on_hand
    if difference == 0:
        return 0

    if difference > 0:
        if product.batches:
            newest = max(product.batches, key=lambda b: b.received_date)
            newest.quantity += difference
        else:
            product.batches.append(Batch(_unique_batch_id(product, f"ADJ-{date}"),
                                         difference, date))
    else:
        if reason == "COUNT" and abs(difference) > 0.2 * on_hand:
            raise ValueError("needs manager approval")
        _take_fifo(product, product.batches, -difference)

    _record(store, sku, "ADJUST", difference, date, reason)
    return difference


def transfer_stock(store: StockStore, sku: str, quantity: int,
                   from_loc: str, to_loc: str, date: str) -> int:
    product = store.get_product(sku)
    if from_loc not in LOCATIONS or to_loc not in LOCATIONS or from_loc == to_loc:
        raise ValueError("invalid source or destination location")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if from_loc == "QUARANTINE" and to_loc != "MAIN":
        raise ValueError("quarantined stock can only be released to MAIN")

    source = sorted((b for b in product.batches if b.location == from_loc), key=_fifo_key)
    if quantity > sum(b.quantity for b in source):
        raise ValueError(f"not enough stock at {from_loc}")

    remaining = quantity
    for batch in source:
        if remaining == 0:
            break
        move = min(batch.quantity, remaining)
        if move == batch.quantity:
            batch.location = to_loc
        else:
            batch.quantity -= move
            product.batches.append(Batch(_unique_batch_id(product, batch.batch_id + "-T"),
                                         move, batch.received_date,
                                         batch.expiry_date, to_loc))
        remaining -= move

    _record(store, sku, "TRANSFER", quantity, date, f"{from_loc}->{to_loc}")
    return sum(b.quantity for b in product.batches if b.location == to_loc)


def reserve_stock(store: StockStore, sku: str, quantity: int, order_ref: str) -> int:
    raise NotImplementedError


def release_reservation(store: StockStore, sku: str, quantity: int,
                        fulfil: bool, date: str) -> int:
    raise NotImplementedError


def process_return(store: StockStore, sku: str, quantity: int, condition: str,
                   days_since_sale: int, date: str) -> str:
    raise NotImplementedError


def check_expiring_batches(store: StockStore, today: str, within_days: int = 30) -> list:
    raise NotImplementedError


def write_off_expired(store: StockStore, today: str, dry_run: bool = False) -> dict:
    raise NotImplementedError
