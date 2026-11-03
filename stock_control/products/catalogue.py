from stock_control.store import Store


def add_product(
        store, sku, name, category, price, quantity=0, cost=0.0, user=''):
    """P1 (Member 1): As Alex, the depot manager, I want to add a new product
    so that we can start selling it.

    Rules:
        1. SKU is in the right format and not already used
        2. Name is filled in
        3. Price is more than 0
        4. Starting quantity is 0 or more
        5. Category must exist
    """
    raise NotImplementedError("P1 add_product is not implemented yet")


def update_product(store, sku, changes, user=''):
    """P2 (Member 1): As Alex, I want to edit a product's details so that I can
    fix a wrong price or name.

    Rules:
        1. Product must exist
        2. Each field is checked
        3. SKU cannot change once the product has stock history
        4. Archived products cannot be edited
    """
    raise NotImplementedError("P2 update_product is not implemented yet")


def remove_product(store, sku, user=''):
    """P3 (Member 1): As Alex, I want to remove products we no longer sell so
    that staff stop offering them.

    Rules:
        1. Delete only if stock is 0 and it has no history
        2. Otherwise archive it
        3. Not allowed if it is on an open order
    """
    raise NotImplementedError("P3 remove_product is not implemented yet")
