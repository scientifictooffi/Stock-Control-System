from stock_control.models import Movement
from stock_control.store import Store

def _use_by_order(batch):
    return (batch.use_by_date is None, batch.use_by_date or "",
            batch.received_date)

def issue_stock(
        store: Store, sku, quantity, warehouse, date, allow_partial=False,
        user=''):
    """M2 (Member 2): As Christen, I want to record items that are sold or sent
    out so that the stock count stays correct.

    Rules:
        1. Quantity is more than 0
        2. Refused if not enough stock (unless part orders are allowed)
        3. Oldest use-by date goes first
        4. Stock never below 0
    """
    product = store.products.get(sku)
    if product is None:
        raise KeyError(f"product {sku} does not exist")

    if (not isinstance(quantity, int) or isinstance(quantity, bool)
            or quantity <= 0):
        raise ValueError("quantity must be a whole number more than 0")

    if warehouse not in store.warehouses:
        raise ValueError(f"warehouse {warehouse} does not exist")

    available = product.stock_by_warehouse.get(warehouse, 0)
    to_issue = quantity
    if quantity > available:
        if not allow_partial:
            raise ValueError(
                f"not enough stock: {available} available, "
                f"{quantity} requested")
        if available == 0:
            raise ValueError(f"no stock of {sku} in {warehouse}")
        to_issue = available

    batches = sorted(
        (b for b in store.batches
         if b.sku == sku and b.warehouse == warehouse and b.quantity > 0),
        key=_use_by_order)
    remaining = to_issue
    used = []
    for batch in batches:
        if remaining == 0:
            break
        taken = min(batch.quantity, remaining)
        batch.quantity -= taken
        remaining -= taken
        used.append(f"{batch.batch_id}:{taken}")
    if remaining > 0:
        used.append(f"no batch:{remaining}")

    product.quantity -= to_issue
    product.stock_by_warehouse[warehouse] = available - to_issue
    store.movements.append(Movement(
        store.next_id("MV", store.movements), sku, "issue", to_issue,
        warehouse, date, user, "issued from " + ", ".join(used)))

    return to_issue
