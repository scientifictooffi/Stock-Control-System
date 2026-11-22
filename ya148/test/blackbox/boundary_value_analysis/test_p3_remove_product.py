import unittest

from stock_control.models import (Category, Movement, OrderLine, Product,
                                  PurchaseOrder)
from stock_control.products.catalogue import remove_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["NEW-0001"] = Product("NEW-0001", "New tap", "Plumbing",
                                         5.0)
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 4.5, 2.0, 10)
    store.products["HIS-0001"] = Product("HIS-0001", "Sold out valve",
                                         "Plumbing", 3.0)
    store.products["ORD-0001"] = Product("ORD-0001", "Ordered tap",
                                         "Plumbing", 6.0)
    store.products["DON-0001"] = Product("DON-0001", "Delivered tap",
                                         "Plumbing", 6.0)
    store.movements.append(Movement("MV-1", "PIP-0001", "receive", 10,
                                    "Main", "2026-11-03"))
    store.movements.append(Movement("MV-2", "HIS-0001", "receive", 2,
                                    "Main", "2026-11-03"))
    store.movements.append(Movement("MV-3", "HIS-0001", "issue", -2,
                                    "Main", "2026-11-04"))
    store.purchase_orders["PO-1"] = PurchaseOrder(
        "PO-1", "SUP-1", [OrderLine("ORD-0001", 5, 6.0)], "sent")
    store.purchase_orders["PO-2"] = PurchaseOrder(
        "PO-2", "SUP-1", [OrderLine("DON-0001", 5, 6.0)], "received")
    return store


class TestRemoveProductBoundaryValues(unittest.TestCase):

    def test_quantity_zero_no_history_deleted(self):
        store = make_store()
        self.assertEqual("deleted", remove_product(store, "NEW-0001"))

    def test_quantity_one_archived(self):
        store = make_store()
        store.products["NEW-0001"].quantity = 1
        self.assertEqual("archived", remove_product(store, "NEW-0001"))

    def test_quantity_minus_one_archived(self):
        store = make_store()
        store.products["NEW-0001"].quantity = -1
        self.assertEqual("archived", remove_product(store, "NEW-0001"))

    def test_zero_movements_deleted(self):
        store = make_store()
        store.movements.clear()
        self.assertEqual("deleted", remove_product(store, "HIS-0001"))

    def test_one_movement_archived(self):
        store = make_store()
        store.movements = [store.movements[1]]
        self.assertEqual("archived", remove_product(store, "HIS-0001"))

    def test_zero_open_orders_allowed(self):
        store = make_store()
        store.purchase_orders["PO-1"].status = "received"
        self.assertEqual("deleted", remove_product(store, "ORD-0001"))

    def test_one_open_order_rejected(self):
        with self.assertRaises(ValueError):
            remove_product(make_store(), "ORD-0001")

    def test_order_with_zero_lines_allowed(self):
        store = make_store()
        store.purchase_orders["PO-1"].lines = []
        self.assertEqual("deleted", remove_product(store, "ORD-0001"))

    def test_order_with_sku_as_second_line_rejected(self):
        store = make_store()
        store.purchase_orders["PO-1"].lines.append(
            OrderLine("NEW-0001", 1, 5.0))
        with self.assertRaises(ValueError):
            remove_product(store, "NEW-0001")

    def test_empty_store_rejected(self):
        with self.assertRaises(ValueError):
            remove_product(Store(), "NEW-0001")


if __name__ == "__main__":
    unittest.main()
