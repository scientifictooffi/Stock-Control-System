from stock_control.store import Store


def suggest_reorder(store, sku, daily_sales, safety_stock=0):
    """S7 (Member 3): As Bee, I want the system to suggest when and how much to
    reorder so that I don't have to guess.

    Rules:
        1. Reorder point = average daily sales x delivery days + safety stock
        2. Amount rounded up to the supplier's pack size and kept under
           the maximum
        3. No sales history = no suggestion
    """
    raise NotImplementedError("S7 suggest_reorder is not implemented yet")
