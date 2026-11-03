from stock_control.store import Store


def generate_alerts(store):
    """S6 (Member 3): As Bee, I want a list of items that are running low so
    that I know what to order first.

    Rules:
        1. Out of stock = urgent
        2. Below safety level = high
        3. Below reorder level = medium
        4. Otherwise no alert
        5. Archived products are ignored
    """
    raise NotImplementedError("S6 generate_alerts is not implemented yet")
