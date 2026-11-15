from stock_control.models import Movement
from stock_control.store import Store

REASONS = ("damaged", "lost", "count error")
APPROVAL_PERCENT = 10
APPROVAL_VALUE = 500


def adjust_stock(
        store: Store, sku, quantity_change, reason, warehouse, date,
        approved_by=None, user=''):
    """M3 (Member 2): As Alex, I want to record broken or missing items with a
    reason so that the numbers stay honest.

    Rules:
        1. Reason must be damaged, lost or count error
        2. Big changes (over 10% or over 500 pounds) need manager approval
        3. Stock cannot go below 0
    """
    product = store.products.get(sku)
    if product is None:
        raise KeyError(f"product {sku} does not exist")

    if reason not in REASONS:
        raise ValueError("reason must be damaged, lost or count error")

    if (not isinstance(quantity_change, int)
            or isinstance(quantity_change, bool) or quantity_change == 0):
        raise ValueError("change must be a whole number other than 0")

    if warehouse not in store.warehouses:
        raise ValueError(f"warehouse {warehouse} does not exist")

    stock = product.stock_by_warehouse.get(warehouse, 0)
    if stock + quantity_change < 0:
        raise ValueError(
            f"stock cannot go below 0: {stock} in stock, "
            f"change {quantity_change}")

    size = abs(quantity_change)
    if (size * 100 > APPROVAL_PERCENT * stock
            or round(size * product.cost, 2) > APPROVAL_VALUE):
        approver = store.users.get(approved_by)
        if (approver is None or approver.role != "manager"
                or not approver.active):
            raise ValueError("this change needs manager approval")

    product.quantity += quantity_change
    product.stock_by_warehouse[warehouse] = stock + quantity_change
    note = reason if approved_by is None else (
        f"{reason}, approved by {approved_by}")
    store.movements.append(Movement(
        store.next_id("MV", store.movements), sku, "adjust", quantity_change,
        warehouse, date, user, note))

    return stock + quantity_change
