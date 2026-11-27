from datetime import date as _date
from math import floor

from stock_control.models import Movement


def _valid_date(value):
    try:
        parsed = _date.fromisoformat(value)
    except (TypeError, ValueError):
        return False
    return parsed.isoformat() == value


def receive_against_po(store, po_id, received, warehouse, date, user=''):
    """S5 (Member 3): As Alex, I want to check a delivery against its order
    so that we only pay for what arrived.

    Rules:
        1. Order must have been sent.
        2. Part delivery records only the quantity received.
        3. Full delivery closes the order.
        4. Up to 5% extra is accepted; more is refused.

    Details:
        - Quantities in ``received`` are this delivery's quantities by SKU.
        - The 5% allowance is cumulative for each order line.
        - Invalid deliveries are rejected before stock or order data changes.
        - Successful receipts update product stock and inbound movements.

    Returns:
        The updated PurchaseOrder.
    """
    order = store.purchase_orders.get(po_id)
    if order is None:
        raise KeyError(f"purchase order {po_id} does not exist")
    if order.status not in ('sent', 'partially_received'):
        raise ValueError("purchase order must be sent before receiving")
    if not isinstance(warehouse, str) or not warehouse.strip():
        raise ValueError("warehouse is required")
    if warehouse not in store.warehouses:
        raise KeyError(f"warehouse {warehouse} does not exist")
    if not _valid_date(date):
        raise ValueError("date must be a valid YYYY-MM-DD date")
    if not isinstance(received, dict) or not received:
        raise ValueError("received must be a non-empty mapping of SKU to quantity")

    lines = {line.sku: line for line in order.lines}
    validated = []
    for sku, quantity in received.items():
        if sku not in lines:
            raise ValueError(f"SKU {sku} is not on purchase order {po_id}")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("received quantities must be whole numbers greater than zero")
        line = lines[sku]
        cumulative = line.received + quantity
        maximum = floor(line.quantity * 1.05)
        if cumulative > maximum:
            raise ValueError(f"received quantity for {sku} exceeds the 5% allowance")
        product = store.products.get(sku)
        if product is None:
            raise KeyError(f"product {sku} does not exist")
        validated.append((line, product, sku, quantity))

    # Apply only after the entire delivery has passed validation.
    for line, product, sku, quantity in validated:
        line.received += quantity
        product.quantity += quantity
        product.stock_by_warehouse[warehouse] = product.stock_by_warehouse.get(warehouse, 0) + quantity
        movement_id = store.next_id('MV', store.movements)
        store.movements.append(Movement(movement_id, sku, 'IN', quantity, warehouse, date, user, f'Received against {po_id}'))

    order.status = 'received' if all(line.received >= line.quantity for line in order.lines) else 'partially_received'
    return order
