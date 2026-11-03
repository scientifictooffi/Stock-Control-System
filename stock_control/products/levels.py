from stock_control.store import Store


def set_stock_levels(store, sku, min_level, max_level, reorder_level):
    """P6 (Member 1): As Bee the buyer, I want to set the lowest and highest
    stock level for each product so that we know when to reorder.

    Rules:
        1. Minimum is 0 or more
        2. Maximum is bigger than minimum
        3. Reorder level is between them
        4. Warning if stock is already below the minimum
    """
    raise NotImplementedError("P6 set_stock_levels is not implemented yet")
