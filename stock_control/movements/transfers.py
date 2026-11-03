from stock_control.store import Store


def transfer_stock(
        store, sku, quantity, from_warehouse, to_warehouse, action='create',
        transfer_id=None, user=''):
    """M4 (Member 2): As Alex, I want to move stock from one warehouse to the
    other so that each site has what it needs.

    Rules:
        1. From and to must be different
        2. Both warehouses exist
        3. Enough stock at the sending site
        4. Status: pending, in transit, received
        5. Cancel returns stock
    """
    raise NotImplementedError("M4 transfer_stock is not implemented yet")
