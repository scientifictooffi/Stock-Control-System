import copy
from stock_control.models import Batch, Product, Warehouse
from stock_control.store import Store

TODAY = "2026-11-11"
SKU = "PIP-0001"
OTHER_SKU = "TAP-0001"
UNKNOWN_SKU = "XYZ-9999"
MAIN_QTY = 10

def make_store():
    store = Store()
    store.warehouses = {
        "MAIN": Warehouse("MAIN", "Main warehouse"),
        "NORTH": Warehouse("NORTH", "North warehouse"),
    }
    store.products = {
        SKU: Product(
            SKU, "Copper pipe 15mm", "Plumbing", 9.99, cost=6.0,
            quantity=MAIN_QTY, stock_by_warehouse={"MAIN": MAIN_QTY}),
        OTHER_SKU: Product(
            OTHER_SKU, "Basin tap", "Plumbing", 24.0, cost=15.0,
            quantity=5, stock_by_warehouse={"MAIN": 5}),
    }
    store.batches = [
        Batch("B0001", SKU, "MAIN", 4, "2026-11-01", "2026-12-20"),
        Batch("B0002", SKU, "MAIN", 3, "2026-11-05", "2026-11-20"),
        Batch("B0003", SKU, "MAIN", 2, "2026-10-01", None),
        Batch("B0004", OTHER_SKU, "MAIN", 5, "2026-11-02", "2026-11-15"),
    ]
    return store


def batch(store, batch_id):
    return next(b for b in store.batches if b.batch_id == batch_id)


def snapshot(store):
    return copy.deepcopy(store)
