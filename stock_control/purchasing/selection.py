from stock_control.store import Store


def select_best_supplier(store, sku, quantity):
    """S8 (Member 3): As Bee, I want to see the best supplier for a product so
    that I get good value and fast delivery.

    Rules:
        1. Score uses price, delivery time and rating
        2. Suspended suppliers left out
        3. A tie goes to the preferred supplier, then the cheapest
        4. Error if no one sells it
    """
    raise NotImplementedError("S8 select_best_supplier is not implemented yet")
