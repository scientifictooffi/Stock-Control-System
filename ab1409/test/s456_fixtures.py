from stock_control.models import Product, PurchaseOrder, OrderLine, User, Warehouse
from stock_control.store import Store

DATE = '2026-11-25'
SKU_A = 'SKU-A'
SKU_B = 'SKU-B'
PO_ID = 'PO0001'


def make_store(total=800.0, status='draft', quantity=10, min_level=5, reorder_level=8):
    store = Store()
    store.products = {
        SKU_A: Product(SKU_A, 'Widget A', 'Tools', 10.0, quantity=quantity,
                       min_level=min_level, reorder_level=reorder_level),
        SKU_B: Product(SKU_B, 'Widget B', 'Tools', 10.0, quantity=0,
                       min_level=4, reorder_level=7),
        'OLD': Product('OLD', 'Archived item', 'Tools', 2.0, quantity=0,
                       min_level=5, reorder_level=8, status='archived'),
    }
    store.warehouses = {'MAIN': Warehouse('MAIN', 'Main warehouse')}
    store.users = {
        'manager1': User('manager1', 'x', 'manager'),
        'owner1': User('owner1', 'x', 'admin'),
        'buyer1': User('buyer1', 'x', 'buyer'),
    }
    store.purchase_orders[PO_ID] = PurchaseOrder(
        PO_ID, 'SUP0001', [OrderLine(SKU_A, 10, 10.0)], status,
        DATE, total, total * 1.2)
    return store
