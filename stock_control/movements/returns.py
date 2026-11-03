from stock_control.store import Store


def process_return(
        store, sku, quantity, sold_quantity, sale_date, return_date,
        condition, warehouse, user=''):
    """M8 (Member 2): As Christen, I want to handle customer returns so that
    good items go back on the shelf.

    Rules:
        1. Must be within 30 days
        2. Good items go back into stock
        3. Damaged items are kept aside
        4. After 30 days refused
        5. Cannot return more than was bought
    """
    raise NotImplementedError("M8 process_return is not implemented yet")
