import copy
from stock_control.models import Product, User, Warehouse
from stock_control.store import Store

TODAY = "2026-11-14"
SKU = "PIP-0001"
DEAR_SKU = "TAP-0001"
UNKNOWN_SKU = "XYZ-9999"
MAIN_QTY = 50


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
        DEAR_SKU: Product(
            DEAR_SKU, "Designer basin tap", "Plumbing", 400.0, cost=250.0,
            quantity=100, stock_by_warehouse={"MAIN": 100}),
    }
    store.users = {
        "kim": User("kim", "pass123", "manager"),
        "sam": User("sam", "pass123", "staff"),
        "lee": User("lee", "pass123", "manager", active=False),
    }
    return store


def snapshot(store):
    return copy.deepcopy(store)
