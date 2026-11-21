from stock_control.models import Category, Product, User, Warehouse
from stock_control.store import Store

DEMO_USERS = (
    ("admin", "admin123", "admin"),
    ("manager", "manager123", "manager"),
    ("clerk", "clerk123", "clerk"),
)
DEMO_WAREHOUSES = (("MAIN", "Main depot"), ("NORTH", "North yard"))
DEMO_CATEGORIES = ("Plumbing", "Electrical", "Timber", "Tools", "Fixings")
DEMO_PRODUCTS = (
    ("PIP-0001", "Copper pipe 15mm 3m", "Plumbing", 8.5, 4.2, 40),
    ("TAP-0001", "Brass garden tap", "Plumbing", 12.0, 6.0, 15),
    ("CAB-0001", "Twin and earth cable 2.5mm 50m", "Electrical", 45.0,
     28.0, 6),
    ("TIM-0001", "CLS timber 38x89 2.4m", "Timber", 4.75, 2.9, 120),
    ("DRL-0001", "Cordless drill 18V", "Tools", 89.0, 55.0, 3),
    ("SCR-0001", "Wood screws 4x40 box 200", "Fixings", 6.2, 3.1, 0),
)


def seed_demo_data(store):
    if store.users:
        return store
    for username, password, role in DEMO_USERS:
        store.users[username] = User(username, password, role)
    for code, name in DEMO_WAREHOUSES:
        store.warehouses[code] = Warehouse(code, name)
    for name in DEMO_CATEGORIES:
        store.categories[name] = Category(name)
    for sku, name, category, price, cost, quantity in DEMO_PRODUCTS:
        store.products[sku] = Product(
            sku, name, category, price, cost, quantity, min_level=5,
            max_level=200, reorder_level=10,
            stock_by_warehouse={"MAIN": quantity})
    return store


def demo_store():
    return seed_demo_data(Store())
