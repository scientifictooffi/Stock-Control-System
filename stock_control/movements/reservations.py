from stock_control.store import Store


def reserve_stock(
        store, sku, quantity, customer, today, hold_days=7, action='create',
        reservation_id=None):
    """M7 (Member 2): As Christen, I want to hold stock for a customer who has
    paid a deposit so that it is not sold to someone else.

    Rules:
        1. Free stock = in stock minus already held
        2. Refused if not enough is free
        3. Hold ends after X days
        4. Cancelling frees the stock
    """
    raise NotImplementedError("M7 reserve_stock is not implemented yet")
