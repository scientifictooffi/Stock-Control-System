from stock_control.store import Store


def convert_quantity(store, sku, quantity, from_unit, to_unit):
    """P9 (Member 1): As Christen, I want to sell items as singles or by the
    box so that stock goes down by the right amount.

    Rules:
        1. Box size must be set for the product
        2. Result must be whole items
        3. Unknown unit is rejected
        4. Same unit gives the same number back
    """
    raise NotImplementedError("P9 convert_quantity is not implemented yet")
