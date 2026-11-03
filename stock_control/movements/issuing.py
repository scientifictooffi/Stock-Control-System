from stock_control.store import Store


def issue_stock(
        store, sku, quantity, warehouse, date, allow_partial=False, user=''):
    """M2 (Member 2): As Christen, I want to record items that are sold or sent
    out so that the stock count stays correct.

    Rules:
        1. Quantity is more than 0
        2. Refused if not enough stock (unless part orders are allowed)
        3. Oldest use-by date goes first
        4. Stock never below 0
    """
    raise NotImplementedError("M2 issue_stock is not implemented yet")
