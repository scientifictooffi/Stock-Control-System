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


class TestRemoveProductConcolic(unittest.TestCase):

    def test_iteration_0_seed_delete(self):
        store = make_store()
        self.assertEqual("deleted", remove_product(store, "NEW-0001"))

    def test_iteration_1_negate_no_history(self):
        store = make_store()
        self.assertEqual("archived", remove_product(store, "HIS-0001"))

    def test_iteration_2_negate_quantity_zero(self):
        store = make_store()
        self.assertEqual("archived", remove_product(store, "PIP-0001"))

    def test_iteration_3_negate_order_has_other_sku(self):
        with self.assertRaises(ValueError):
            remove_product(make_store(), "ORD-0001")

    def test_iteration_4_negate_order_status_open(self):
        store = make_store()
        self.assertEqual("deleted", remove_product(store, "DON-0001"))

    def test_iteration_5_negate_product_exists(self):
        with self.assertRaises(ValueError):
            remove_product(make_store(), "NOP-0000")


if __name__ == "__main__":
    unittest.main()
