import copy
from stock_control.models import Product, Transfer, Warehouse
from stock_control.store import Store

TODAY = "2026-11-23"
SKU = "PIP-0001"
UNKNOWN_SKU = "XYZ-9999"
MAIN_QTY = 50
NORTH_QTY = 5


def make_store():
    store = Store()
    store.warehouses = {
        "MAIN": Warehouse("MAIN", "Main warehouse"),
        "NORTH": Warehouse("NORTH", "North warehouse"),
    }
    store.products = {
        SKU: Product(
            SKU, "Copper pipe 15mm", "Plumbing", 9.99, cost=6.0,
            quantity=MAIN_QTY + NORTH_QTY,
            stock_by_warehouse={"MAIN": MAIN_QTY, "NORTH": NORTH_QTY}),
    }
    return store


def add_transfer(store, status, quantity=10, transfer_id="TR0001"):
    store.products[SKU].stock_by_warehouse["MAIN"] -= quantity
    store.transfers[transfer_id] = Transfer(
        transfer_id, SKU, quantity, "MAIN", "NORTH", status)
    return store


def stock(store, warehouse):
    return store.products[SKU].stock_by_warehouse.get(warehouse, 0)


def snapshot(store):
    return copy.deepcopy(store)
