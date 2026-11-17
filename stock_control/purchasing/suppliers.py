import math
import re

from stock_control.models import ProductSupplier, Supplier
from stock_control.store import Store

SUPPLIER_STATUSES = ("active", "suspended")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]+$")
MIN_PHONE_DIGITS = 7
MAX_PHONE_DIGITS = 15
MIN_LEAD_TIME_DAYS = 1
MAX_LEAD_TIME_DAYS = 90


def _is_valid_email(email):
    if not isinstance(email, str):
        return False
    return EMAIL_PATTERN.match(email.strip()) is not None


def _is_valid_phone(phone):
    """A phone number is digits with optional +, spaces, brackets, dashes."""
    if not isinstance(phone, str):
        return False
    text = phone.strip()
    if PHONE_PATTERN.match(text) is None:
        return False
    digits = sum(1 for character in text if character.isdigit())
    return MIN_PHONE_DIGITS <= digits <= MAX_PHONE_DIGITS


def _name_in_use(store, name, own_id):
    """True when another supplier already uses this name (any letter case)."""
    wanted = name.casefold()
    return any(
        other.name.casefold() == wanted
        for other_id, other in store.suppliers.items()
        if other_id != own_id)


def save_supplier(
        store, name, email, phone, status='active', supplier_id=None):
    """S1 (Member 3): As Bee the buyer, I want to save supplier details so that
    I can contact them easily.

    Rules:
        1. Supplier name is not already used
        2. Email and phone number are valid
        3. Status is active or suspended
        4. Suspended suppliers can only be reactivated

    Details:
        - supplier_id=None adds a new supplier (id SUP0001, SUP0002, ...).
          A supplier_id of an existing supplier edits that supplier. An
          unknown supplier_id raises KeyError. Every other broken rule raises
          ValueError and nothing is changed.
        - Name is required. Names are compared ignoring capital letters and
          surrounding spaces, so "Acme Ltd" and " acme ltd " are the same.
          A supplier may keep its own name when it is edited.
        - Email must look like name@domain.tld. Phone may contain digits, one
          leading +, spaces, brackets and dashes, with 7 to 15 digits.
        - Status must be "active" or "suspended".
        - A suspended supplier can only be reactivated: the call must set
          status "active" and leave name, email and phone unchanged.

    Returns:
        The saved Supplier.
    """
    existing = None
    if supplier_id is not None:
        existing = store.suppliers.get(supplier_id)
        if existing is None:
            raise KeyError(f"supplier {supplier_id} does not exist")

    if not isinstance(name, str) or name.strip() == "":
        raise ValueError("name is required")
    name = name.strip()
    if _name_in_use(store, name, supplier_id):
        raise ValueError(f"supplier name {name} is already used")
    if not _is_valid_email(email):
        raise ValueError("email is not valid")
    if not _is_valid_phone(phone):
        raise ValueError("phone number is not valid")
    if status not in SUPPLIER_STATUSES:
        raise ValueError("status must be active or suspended")
    email = email.strip()
    phone = phone.strip()

    if existing is None:
        supplier = Supplier(
            store.next_id("SUP", store.suppliers), name, email, phone, status)
        store.suppliers[supplier.supplier_id] = supplier
        return supplier

    if existing.status == "suspended":
        if status != "active":
            raise ValueError("a suspended supplier can only be reactivated")
        if (name, email, phone) != (
                existing.name, existing.email, existing.phone):
            raise ValueError(
                "a suspended supplier can only be reactivated, "
                "details cannot be changed")
    existing.name = name
    existing.email = email
    existing.phone = phone
    existing.status = status
    return existing


def _is_whole_number(value):
    return isinstance(value, int) and not isinstance(value, bool)


def link_product_supplier(
        store, sku, supplier_id, price, lead_time_days, preferred=False,
        pack_size=1):
    """S2 (Member 3): As Bee, I want to record which supplier sells each
    product and at what price so that I can compare them.

    Rules:
        1. Product and supplier exist and are active
        2. Price is more than 0
        3. Delivery time is 1 to 90 days
        4. Only one preferred supplier per product

    Details:
        - Unknown SKU or unknown supplier raises KeyError. Every other broken
          rule raises ValueError and nothing is changed.
        - Price is a number (not bool) more than 0 and not infinite.
        - Delivery time (lead_time_days) is a whole number from 1 to 90,
          both ends included.
        - pack_size is a whole number of 1 or more. preferred is True/False.
        - If the product is already linked to this supplier, that link is
          updated instead of adding a second one.
        - Setting preferred=True is refused while a different supplier is
          already the preferred one for this product. To change the
          preferred supplier, first save the old link with preferred=False.
        - product.preferred_supplier always shows the preferred supplier's id,
          or None when no link is preferred.

    Returns:
        The saved ProductSupplier.
    """
    product = store.products.get(sku)
    if product is None:
        raise KeyError(f"product {sku} does not exist")
    if product.status != "active":
        raise ValueError(f"product {sku} is not active")
    supplier = store.suppliers.get(supplier_id)
    if supplier is None:
        raise KeyError(f"supplier {supplier_id} does not exist")
    if supplier.status != "active":
        raise ValueError(f"supplier {supplier_id} is not active")

    if (not isinstance(price, (int, float)) or isinstance(price, bool)
            or not math.isfinite(price) or price <= 0):
        raise ValueError("price must be more than 0")
    if (not _is_whole_number(lead_time_days)
            or not MIN_LEAD_TIME_DAYS <= lead_time_days <= MAX_LEAD_TIME_DAYS):
        raise ValueError("delivery time must be 1 to 90 days")
    if not _is_whole_number(pack_size) or pack_size < 1:
        raise ValueError("pack size must be a whole number of 1 or more")
    if not isinstance(preferred, bool):
        raise ValueError("preferred must be True or False")

    links = [link for link in store.product_suppliers if link.sku == sku]
    if preferred and any(
            link.preferred and link.supplier_id != supplier_id
            for link in links):
        raise ValueError(
            f"product {sku} already has a preferred supplier")

    link = next(
        (item for item in links if item.supplier_id == supplier_id), None)
    if link is None:
        link = ProductSupplier(
            sku, supplier_id, price, lead_time_days, pack_size, preferred)
        store.product_suppliers.append(link)
    else:
        link.price = price
        link.lead_time_days = lead_time_days
        link.pack_size = pack_size
        link.preferred = preferred

    preferred_ids = [
        item.supplier_id for item in store.product_suppliers
        if item.sku == sku and item.preferred]
    product.preferred_supplier = preferred_ids[0] if preferred_ids else None
    return link
