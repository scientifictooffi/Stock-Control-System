from stock_control.store import Store


def receive_stock(
        store, sku, quantity, warehouse, date, use_by_date=None, user=''):
    """M1 (Member 2): As Alex, I want to record a delivery when it arrives so
    that the new stock shows up straight away.

    Rules:
        1. Product exists and is active
        2. Quantity is more than 0
        3. Warehouse exists
        4. Use-by date (if given) is not in the past
        5. Stock and history updated
    """
    raise NotImplementedError("M1 receive_stock is not implemented yet")
