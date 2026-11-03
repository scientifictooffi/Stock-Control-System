from stock_control.store import Store


def adjust_stock(
        store, sku, quantity_change, reason, warehouse, date,
        approved_by=None, user=''):
    """M3 (Member 2): As Alex, I want to record broken or missing items with a
    reason so that the numbers stay honest.

    Rules:
        1. Reason must be damaged, lost or count error
        2. Big changes (over 10% or over 500 pounds) need manager approval
        3. Stock cannot go below 0
    """
    raise NotImplementedError("M3 adjust_stock is not implemented yet")
