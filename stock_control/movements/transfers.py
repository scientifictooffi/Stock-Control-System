from stock_control.models import Movement, Transfer
from stock_control.store import Store

PENDING = "pending"
IN_TRANSIT = "in transit"
RECEIVED = "received"
CANCELLED = "cancelled"

ALLOWED_FROM = {
    "dispatch": (PENDING,),
    "receive": (IN_TRANSIT,),
    "cancel": (PENDING, IN_TRANSIT),
}


def transfer_stock(
        store: Store, sku, quantity, from_warehouse, to_warehouse,
        action='create', transfer_id=None, user='', date=''):
    """M4 (Member 2): As Alex, I want to move stock from one warehouse to the
    other so that each site has what it needs.

    Rules:
        1. From and to must be different
        2. Both warehouses exist
        3. Enough stock at the sending site
        4. Status: pending, in transit, received
        5. Cancel returns stock
    """
    if action == "create":
        product = store.products.get(sku)
        if product is None:
            raise KeyError(f"product {sku} does not exist")

        if (not isinstance(quantity, int) or isinstance(quantity, bool)
                or quantity <= 0):
            raise ValueError("quantity must be a whole number more than 0")

        if from_warehouse == to_warehouse:
            raise ValueError("from and to warehouse must be different")

        if (from_warehouse not in store.warehouses
                or to_warehouse not in store.warehouses):
            raise ValueError("both warehouses must exist")

        available = product.stock_by_warehouse.get(from_warehouse, 0)
        if quantity > available:
            raise ValueError(
                f"not enough stock in {from_warehouse}: {available} "
                f"available, {quantity} requested")

        product.stock_by_warehouse[from_warehouse] = available - quantity
        transfer = Transfer(
            store.next_id("TR", store.transfers), sku, quantity,
            from_warehouse, to_warehouse, PENDING)
        store.transfers[transfer.transfer_id] = transfer
        store.movements.append(Movement(
            store.next_id("MV", store.movements), sku, "transfer out",
            quantity, from_warehouse, date, user,
            f"{transfer.transfer_id} to {to_warehouse}"))
        return transfer

    allowed = ALLOWED_FROM.get(action)
    if allowed is None:
        raise ValueError(
            "action must be create, dispatch, receive or cancel")

    transfer = store.transfers.get(transfer_id)
    if transfer is None:
        raise KeyError(f"transfer {transfer_id} does not exist")

    if transfer.status not in allowed:
        raise ValueError(
            f"cannot {action} a transfer that is {transfer.status}")

    if action == "dispatch":
        transfer.status = IN_TRANSIT
        return transfer

    if action == "receive":
        warehouse = transfer.to_warehouse
        transfer.status = RECEIVED
        kind, note = "transfer in", f"{transfer.transfer_id} received"
    else:
        warehouse = transfer.from_warehouse
        transfer.status = CANCELLED
        kind, note = "transfer cancel", f"{transfer.transfer_id} cancelled"

    product = store.products[transfer.sku]
    product.stock_by_warehouse[warehouse] = (
        product.stock_by_warehouse.get(warehouse, 0) + transfer.quantity)
    store.movements.append(Movement(
        store.next_id("MV", store.movements), transfer.sku, kind,
        transfer.quantity, warehouse, date, user, note))
    return transfer
