from datetime import date as _date
from stock_control.models import Batch, Movement
from stock_control.store import Store


def _parse_date(value, field_name):
    """Turn a YYYY-MM-DD string into a date, or raise ValueError.

    The round-trip check keeps this strict on every Python version:
    from 3.11 fromisoformat also accepts forms such as "20261107".
    """
    try:
        parsed = _date.fromisoformat(value)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None or parsed.isoformat() != value:
        raise ValueError(f"{field_name} must be a date in YYYY-MM-DD format")
    return parsed


def receive_stock(
        store: Store, sku, quantity, warehouse, date, use_by_date=None,
        user=''):
    """M1 (Member 2): As Alex, I want to record a delivery when it arrives so
    that the new stock shows up straight away.

    Rules:
        1. Product exists and is active
        2. Quantity is more than 0
        3. Warehouse exists
        4. Use-by date (if given) is not in the past
        5. Stock and history updated

    Details:
        - Unknown SKU raises KeyError. Every other broken rule raises
          ValueError and nothing is changed.
        - Quantity must be a whole number (int, not bool or float).
        - date and use_by_date are YYYY-MM-DD strings. "Not in the past"
          means use_by_date is on or after date, so a use-by date equal to
          the delivery date is accepted.
        - On success: the product's total quantity and its quantity in that
          warehouse go up, a new Batch is added to store.batches, and a
          "receive" Movement is added to store.movements.

    Returns:
        The product's new total quantity.
    """
    product = store.products.get(sku)
    if product is None:
        raise KeyError(f"product {sku} does not exist")
    if product.status != "active":
        raise ValueError(f"product {sku} is not active")

    if (not isinstance(quantity, int) or isinstance(quantity, bool)
            or quantity <= 0):
        raise ValueError("quantity must be a whole number more than 0")

    if warehouse not in store.warehouses:
        raise ValueError(f"warehouse {warehouse} does not exist")

    received_on = _parse_date(date, "date")
    if use_by_date is not None:
        if _parse_date(use_by_date, "use-by date") < received_on:
            raise ValueError("use-by date is in the past")

    product.quantity += quantity
    product.stock_by_warehouse[warehouse] = (
        product.stock_by_warehouse.get(warehouse, 0) + quantity)

    batch_id = store.next_id("B", store.batches)
    store.batches.append(Batch(
        batch_id, sku, warehouse, quantity, date, use_by_date))
    store.movements.append(Movement(
        store.next_id("MV", store.movements), sku, "receive", quantity,
        warehouse, date, user, f"delivery {batch_id}"))

    return product.quantity
