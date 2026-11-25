import copy
from stock_control.models import Product, ProductSupplier, Supplier
from stock_control.store import Store

TODAY = "2026-11-07"
PIPE_SKU = "PIP-0001"
TAP_SKU = "TAP-0002"
BRICK_SKU = "BRK-0003"
UNKNOWN_SKU = "XYZ-9999"
ACME = "SUP0001"          # active, minimum order 50.00, sells pipe and tap
SUSPENDED_ID = "SUP0002"  # suspended, sells brick
DELTA = "SUP0003"         # active, no minimum, sells pipe and brick
UNKNOWN_ID = "SUP9999"


def make_store():
    store = Store()
    store.products = {
        PIPE_SKU: Product(PIPE_SKU, "Copper pipe 15mm", "Plumbing", 15.0),
        TAP_SKU: Product(TAP_SKU, "Basin tap", "Plumbing", 24.50),
        BRICK_SKU: Product(BRICK_SKU, "Facing brick", "Building", 0.99),
    }
    store.suppliers = {
        ACME: Supplier(ACME, "Acme Plumbing Ltd", "a@acme.co", "01164960001",
                       min_order_value=50.0),
        SUSPENDED_ID: Supplier(
            SUSPENDED_ID, "Sigma Ltd", "s@sigma.co", "01164960002",
            status="suspended"),
        DELTA: Supplier(DELTA, "Delta Tools", "d@delta.co", "01164960003"),
    }
    store.product_suppliers = [
        ProductSupplier(PIPE_SKU, ACME, 10.00, 3),
        ProductSupplier(TAP_SKU, ACME, 5.50, 3),
        ProductSupplier(BRICK_SKU, SUSPENDED_ID, 0.50, 5),
        ProductSupplier(PIPE_SKU, DELTA, 12.00, 7),
        ProductSupplier(BRICK_SKU, DELTA, 3.33, 7),
    ]
    return store


def snapshot(store):
    return copy.deepcopy(store)
