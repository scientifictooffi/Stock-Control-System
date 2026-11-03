from stock_control.store import Store


def reconcile_count(store, counted, warehouse, date):
    """M5 (Member 2): As Alex, I want to enter our stock count and compare it
    with the system so that I can spot mistakes.

    Rules:
        1. Difference = counted minus system
        2. Up to 2% is accepted
        3. More than 2% is flagged for a recount
        4. Items not counted are listed
    """
    raise NotImplementedError("M5 reconcile_count is not implemented yet")
