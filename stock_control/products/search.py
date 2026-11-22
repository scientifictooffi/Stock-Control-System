from stock_control.store import Store

AVAILABILITY = ("in_stock", "low", "out")


def _availability(product):
    if product.quantity <= 0:
        return "out"
    if product.quantity < product.min_level:
        return "low"
    return "in_stock"


def search_products(
        store, name='', category=None, min_price=None, max_price=None,
        availability=None):
    """P4 (Member 1): As a trade counter assistant, I want to search for a
    product by name so that I can quickly tell a customer whether we have it
    in stock.

    Rules:
        1. Part of the name is enough
        2. Not case sensitive
        3. Can filter by category, price and in stock / low / out
        4. Message if nothing is found

    Returns the matching active products sorted by name. Raises ValueError
    for a bad filter and LookupError when nothing matches.
    """
    if not isinstance(name, str):
        raise ValueError("name must be text")
    if category is not None and category not in store.categories:
        raise ValueError(f"category {category} does not exist")
    if min_price is not None and min_price < 0:
        raise ValueError("minimum price cannot be negative")
    if max_price is not None and max_price < 0:
        raise ValueError("maximum price cannot be negative")
    if (min_price is not None and max_price is not None
            and min_price > max_price):
        raise ValueError("minimum price is above maximum price")
    if availability is not None and availability not in AVAILABILITY:
        raise ValueError("availability must be in_stock, low or out")
    needle = name.strip().lower()
    found = []
    for product in store.products.values():
        if product.status == "archived":
            continue
        if needle and needle not in product.name.lower():
            continue
        if category is not None and product.category != category:
            continue
        if min_price is not None and product.price < min_price:
            continue
        if max_price is not None and product.price > max_price:
            continue
        if (availability is not None
                and _availability(product) != availability):
            continue
        found.append(product)
    if not found:
        raise LookupError("no products match the search")
    return sorted(found, key=lambda product: product.name.lower())
