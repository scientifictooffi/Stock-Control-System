import re

from stock_control.models import Product
from stock_control.store import Store

SKU_PATTERN = re.compile(r"^[A-Z]{3}-[0-9]{4}$")
EDITABLE_FIELDS = ("sku", "name", "category", "price", "cost")


def _is_valid_sku(sku):
    if not isinstance(sku, str):
        return False
    return SKU_PATTERN.match(sku) is not None


def _has_stock_history(store, sku):
    return any(movement.sku == sku for movement in store.movements)


def _check_change(store, product, field, value):
    if field == "sku":
        if _has_stock_history(store, product.sku):
            raise ValueError("SKU cannot change once the product has "
                             "stock history")
        if not _is_valid_sku(value):
            raise ValueError("invalid SKU format, expected ABC-0001")
        if value in store.products:
            raise ValueError(f"SKU {value} already exists")
        return value
    if field == "name":
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("name is required")
        return value.strip()
    if field == "category":
        if value not in store.categories:
            raise ValueError(f"category {value} does not exist")
        return value
    if field == "price":
        if value <= 0:
            raise ValueError("price must be more than 0")
        return value
    if value < 0:
        raise ValueError("cost cannot be negative")
    return value


def add_product(
        store, sku, name, category, price, quantity=0, cost=0.0, user=''):
    """P1 (Member 1): As Alex, the depot manager, I want to add a new product
    so that we can start selling it.

    Rules:
        1. SKU is in the right format (ABC-0001) and not already used
        2. Name is filled in
        3. Price is more than 0
        4. Starting quantity is 0 or more
        5. Category must exist

    Returns the created Product. Raises ValueError when a rule fails.
    """
    if not _is_valid_sku(sku):
        raise ValueError("invalid SKU format, expected ABC-0001")
    if sku in store.products:
        raise ValueError(f"SKU {sku} already exists")
    if not isinstance(name, str) or name.strip() == "":
        raise ValueError("name is required")
    if price <= 0:
        raise ValueError("price must be more than 0")
    if quantity < 0:
        raise ValueError("starting quantity cannot be negative")
    if category not in store.categories:
        raise ValueError(f"category {category} does not exist")
    product = Product(sku=sku, name=name.strip(), category=category,
                      price=price, cost=cost, quantity=quantity)
    store.products[sku] = product
    return product


def update_product(store, sku, changes, user=''):
    """P2 (Member 1): As Alex, I want to edit a product's details so that I can
    fix a wrong price or name.

    Rules:
        1. Product must exist
        2. Each field is checked
        3. SKU cannot change once the product has stock history
        4. Archived products cannot be edited
    """
    if sku not in store.products:
        raise ValueError(f"product {sku} does not exist")
    product = store.products[sku]
    if product.status == "archived":
        raise ValueError("archived products cannot be edited")
    if not changes:
        raise ValueError("no changes given")
    cleaned = {}
    for field, value in changes.items():
        if field not in EDITABLE_FIELDS:
            raise ValueError(f"field {field} cannot be edited")
        cleaned[field] = _check_change(store, product, field, value)
    for field, value in cleaned.items():
        setattr(product, field, value)
    if "sku" in cleaned:
        del store.products[sku]
        store.products[product.sku] = product
    return product


def remove_product(store, sku, user=''):
    """P3 (Member 1): As Alex, I want to remove products we no longer sell so
    that staff stop offering them.

    Rules:
        1. Delete only if stock is 0 and it has no history
        2. Otherwise archive it
        3. Not allowed if it is on an open order
    """
    raise NotImplementedError("P3 remove_product is not implemented yet")
