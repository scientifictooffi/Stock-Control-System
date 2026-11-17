import re

from stock_control.models import Supplier
from stock_control.store import Store

SUPPLIER_STATUSES = ("active", "suspended")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]+$")
MIN_PHONE_DIGITS = 7
MAX_PHONE_DIGITS = 15


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
    """
    raise NotImplementedError(
        "S2 link_product_supplier is not implemented yet")
