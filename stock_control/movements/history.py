from stock_control.store import Store


def get_movements(
        store, sku=None, warehouse=None, movement_type=None, start_date=None,
        end_date=None):
    """M9 (Member 2): As Alex, I want to see the history of a product's stock
    so that I can find out where items went.

    Rules:
        1. Filter by product, warehouse, type and dates
        2. Start date cannot be after end date
        3. Newest first
        4. Message if nothing is found
    """
    raise NotImplementedError("M9 get_movements is not implemented yet")
