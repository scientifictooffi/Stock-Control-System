from stock_control.store import Store


def check_expiry(store, today, days):
    """M6 (Member 2): As Alex, I want to see which items are close to their
    use-by date so that we sell them before they go off.

    Rules:
        1. Shows batches expiring within N days
        2. Marks expired batches
        3. Expired items cannot be sold
        4. N must be a whole number above 0
    """
    raise NotImplementedError("M6 check_expiry is not implemented yet")
