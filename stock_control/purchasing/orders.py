from stock_control.store import Store


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
    """
    raise NotImplementedError(
        "S3 create_purchase_order is not implemented yet")
