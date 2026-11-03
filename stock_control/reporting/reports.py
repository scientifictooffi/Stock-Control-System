from stock_control.store import Store


def stock_level_report(store, group_by='product', category=None):
    """R3 (Member 4): As Alex, I want a stock report so that I can see what is
    low, out or overstocked.

    Rules:
        1. Group by product or warehouse
        2. Each line shows in stock, low, out or overstocked
        3. Can filter by category
        4. Works when there is no stock
    """
    raise NotImplementedError("R3 stock_level_report is not implemented yet")


def slow_moving_report(store, today, days=90, slow_threshold=5):
    """R7 (Member 4): As Alex, I want a list of items that are not selling so
    that we can put them on offer.

    Rules:
        1. No sales in 90+ days = not moving
        2. Very few sales in 90 days = slow
        3. Otherwise active
        4. Limits can be changed but must be above 0
    """
    raise NotImplementedError("R7 slow_moving_report is not implemented yet")
