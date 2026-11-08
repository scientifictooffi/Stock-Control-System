import copy
from stock_control.models import Product, Warehouse
from stock_control.store import Store

TODAY = "2026-11-07"
ACTIVE_SKU = "PIP-0001"
ARCHIVED_SKU = "OLD-0001"
UNKNOWN_SKU = "XYZ-9999"
START_QTY = 4


def make_store():
    store = Store()
    store.warehouses = {
        "MAIN": Warehouse("MAIN", "Main warehouse"),
        "NORTH": Warehouse("NORTH", "North warehouse"),
    }
    store.products = {
        ACTIVE_SKU: Product(
            ACTIVE_SKU, "Copper pipe 15mm", "Plumbing", 9.99, cost=6.0,
            quantity=START_QTY, stock_by_warehouse={"MAIN": START_QTY}),
        ARCHIVED_SKU: Product(
            ARCHIVED_SKU, "Old tap", "Plumbing", 4.50, status="archived"),
    }
    return store


def snapshot(store):
    return copy.deepcopy(store)
