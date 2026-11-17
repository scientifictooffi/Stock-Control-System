"""Shared test data for R3 stock_level_report tests (Member 4)."""
from stock_control.models import Category, Product, Warehouse
from stock_control.store import Store


def make_product(sku, quantity, min_level=5, max_level=50, **extra):
    """One product in the Tools category with the given stock levels."""
    return Product(sku=sku, name=sku, category="Tools", price=1.0,
                   quantity=quantity, min_level=min_level,
                   max_level=max_level, **extra)


def make_store():
    """Store with two categories, two warehouses and one product for each
    status, plus one archived product:
    TLS-0001 out, TLS-0002 low, TLS-0003 in stock (in two warehouses),
    PNT-0001 overstocked, PNT-0002 in stock with no maximum,
    TLS-0009 archived."""
    store = Store()
    store.categories["Tools"] = Category("Tools")
    store.categories["Paint"] = Category("Paint")
    store.warehouses["WH1"] = Warehouse("WH1", "Main depot")
    store.warehouses["WH2"] = Warehouse("WH2", "Side depot")
    store.products["TLS-0001"] = Product(
        "TLS-0001", "Hammer", "Tools", 9.5, quantity=0,
        min_level=5, max_level=50)
    store.products["TLS-0002"] = Product(
        "TLS-0002", "Nails", "Tools", 2.0, quantity=3,
        min_level=5, max_level=50, stock_by_warehouse={"WH1": 3})
    store.products["TLS-0003"] = Product(
        "TLS-0003", "Screws", "Tools", 3.0, quantity=20,
        min_level=5, max_level=50,
        stock_by_warehouse={"WH1": 15, "WH2": 5})
    store.products["PNT-0001"] = Product(
        "PNT-0001", "Paint", "Paint", 12.0, quantity=80,
        min_level=10, max_level=60, stock_by_warehouse={"WH2": 80})
    store.products["PNT-0002"] = Product(
        "PNT-0002", "Brush", "Paint", 4.0, quantity=10,
        stock_by_warehouse={"WH1": 10})
    store.products["TLS-0009"] = Product(
        "TLS-0009", "Old saw", "Tools", 7.0, quantity=0,
        min_level=5, max_level=50, status="archived")
    return store


def statuses(lines):
    """Map each SKU in a product report to its status."""
    return {line["sku"]: line["status"] for line in lines}
