from stock_control.store import Store


def abc_classify(store, yearly_sales):
    """R5 (Member 4): As David, I want products grouped A, B or C by value so
    that we keep a closer eye on expensive items.

    Rules:
        1. Ranked by yearly sales value
        2. Top 80% of value = A, next 15% = B, rest = C
        3. Unused items = C
        4. Empty list handled
    """
    raise NotImplementedError("R5 abc_classify is not implemented yet")


def turnover_ratio(store, sku, start_date, end_date):
    """R6 (Member 4): As David, I want to see how fast stock sells so that I
    know where money is stuck on the shelves.

    Rules:
        1. Turnover = cost of goods sold / average stock value
        2. If average stock is 0 show 'not available'
        3. Days of stock = 365 / turnover
        4. Dates checked
    """
    raise NotImplementedError("R6 turnover_ratio is not implemented yet")
