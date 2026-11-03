from stock_control.store import Store


def search_products(
        store, name='', category=None, min_price=None, max_price=None,
        availability=None):
    """P4 (Member 1): As Christen at the counter, I want to search for a
    product by name so that I can quickly tell a customer if we have it.

    Rules:
        1. Part of the name is enough
        2. Not case sensitive
        3. Can filter by category, price and in stock / low / out
        4. Message if nothing is found
    """
    raise NotImplementedError("P4 search_products is not implemented yet")
