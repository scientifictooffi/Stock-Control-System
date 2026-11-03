from stock_control.store import Store


def value_inventory(store, method='fifo'):
    """R4 (Member 4): As David, I want to know how much our stock is worth so
    that I can give the figure to our accountant.

    Rules:
        1. Choose FIFO or average cost
        2. Other methods refused
        3. Zero stock = 0 pounds
        4. Shows a total per product and overall
    """
    raise NotImplementedError("R4 value_inventory is not implemented yet")
