import copy
from stock_control.models import Product, ProductSupplier, Supplier
from stock_control.store import Store

PIPE_SKU = "PIP-0001"
TAP_SKU = "TAP-0002"
ARCHIVED_SKU = "OLD-0001"
UNKNOWN_SKU = "XYZ-9999"
ACME = "SUP0001"
DELTA = "SUP0002"
SUSPENDED_ID = "SUP0003"
UNKNOWN_ID = "SUP9999"


def make_store():
    store = Store()
    store.products = {
        PIPE_SKU: Product(PIPE_SKU, "Copper pipe 15mm", "Plumbing", 9.99),
        TAP_SKU: Product(TAP_SKU, "Basin tap", "Plumbing", 24.50),
        ARCHIVED_SKU: Product(
            ARCHIVED_SKU, "Old tap", "Plumbing", 4.50, status="archived"),
    }
    store.suppliers = {
        ACME: Supplier(ACME, "Acme Plumbing Ltd", "a@acme.co", "01164960001"),
        DELTA: Supplier(DELTA, "Delta Tools", "d@delta.co", "01164960002"),
        SUSPENDED_ID: Supplier(
            SUSPENDED_ID, "Sigma Ltd", "s@sigma.co", "01164960003",
            status="suspended"),
    }
    return store


def make_store_with_preferred():
    """PIP-0001 is sold by Acme (preferred) and Delta (not preferred)."""
    store = make_store()
    store.product_suppliers = [
        ProductSupplier(PIPE_SKU, ACME, 5.00, 3, 1, True),
        ProductSupplier(PIPE_SKU, DELTA, 4.80, 10, 1, False),
    ]
    store.products[PIPE_SKU].preferred_supplier = ACME
    return store


def snapshot(store):
    return copy.deepcopy(store)
