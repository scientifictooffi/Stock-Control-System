from datetime import date as _date
from decimal import Decimal, ROUND_HALF_UP

from stock_control.models import OrderLine, PurchaseOrder
from stock_control.store import Store

VAT_RATE = Decimal("0.20")
PENNY = Decimal("0.01")


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


def _to_pounds(amount):
    """Round a Decimal amount to whole pence (halves go up)."""
    return amount.quantize(PENNY, rounding=ROUND_HALF_UP)


def create_purchase_order(store, supplier_id, lines, date):
    """S3 (Member 3): As Bee, I want to create a purchase order so that I can
    order stock from a supplier.

    Rules:
        1. Supplier is active
        2. At least one item
        3. Each item is sold by that supplier
        4. Quantity is more than 0
        5. Total includes 20% VAT
        6. Must meet the supplier's minimum order

    Details:
        - Unknown supplier raises KeyError. Every other broken rule raises
          ValueError and nothing is changed.
        - lines is a list of (sku, quantity) pairs. Quantity must be a whole
          number (int, not bool or float) more than 0. The same SKU cannot
          appear twice.
        - "Sold by that supplier" means a product-supplier link (S2) exists
          for the SKU and the supplier. The unit price is the link's price.
        - date is a YYYY-MM-DD string.
        - total_ex_vat is the sum of quantity x unit price, rounded to the
          penny. total_inc_vat is total_ex_vat x 1.20, rounded to the penny
          (halves go up).
        - The minimum order is compared with total_ex_vat. A total equal to
          the supplier's min_order_value is accepted.
        - On success a PurchaseOrder with status "draft" and id PO0001,
          PO0002, ... is added to store.purchase_orders.

    Returns:
        The new PurchaseOrder.
    """
    supplier = store.suppliers.get(supplier_id)
    if supplier is None:
        raise KeyError(f"supplier {supplier_id} does not exist")
    if supplier.status != "active":
        raise ValueError(f"supplier {supplier_id} is not active")
    if not lines:
        raise ValueError("an order needs at least one item")
    _parse_date(date, "date")

    sold = {
        link.sku: link for link in store.product_suppliers
        if link.supplier_id == supplier_id}
    order_lines = []
    seen = set()
    total = Decimal("0")
    for item in lines:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise ValueError("each item must be a (sku, quantity) pair")
        sku, quantity = item
        if sku not in sold:
            raise ValueError(
                f"product {sku} is not sold by supplier {supplier_id}")
        if (not isinstance(quantity, int) or isinstance(quantity, bool)
                or quantity <= 0):
            raise ValueError("quantity must be a whole number more than 0")
        if sku in seen:
            raise ValueError(f"product {sku} appears more than once")
        seen.add(sku)
        unit_price = sold[sku].price
        order_lines.append(OrderLine(sku, quantity, unit_price))
        total += Decimal(str(unit_price)) * quantity

    total_ex_vat = _to_pounds(total)
    if total_ex_vat < Decimal(str(supplier.min_order_value)):
        raise ValueError(
            f"order total {total_ex_vat} is below the supplier's minimum "
            f"order of {supplier.min_order_value}")
    total_inc_vat = _to_pounds(total_ex_vat * (1 + VAT_RATE))

    po_id = store.next_id("PO", store.purchase_orders)
    order = PurchaseOrder(
        po_id, supplier_id, order_lines, "draft", date,
        float(total_ex_vat), float(total_inc_vat))
    store.purchase_orders[po_id] = order
    return order
