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


class TestRemoveProductEquivalencePartitioning(unittest.TestCase):

    def test_no_stock_no_history_is_deleted(self):
        store = make_store()
        result = remove_product(store, "NEW-0001")
        self.assertEqual("deleted", result)
        self.assertNotIn("NEW-0001", store.products)

    def test_stock_present_is_archived(self):
        store = make_store()
        result = remove_product(store, "PIP-0001")
        self.assertEqual("archived", result)
        self.assertEqual("archived", store.products["PIP-0001"].status)

    def test_no_stock_but_history_is_archived(self):
        store = make_store()
        result = remove_product(store, "HIS-0001")
        self.assertEqual("archived", result)
        self.assertIn("HIS-0001", store.products)

    def test_on_open_order_is_rejected(self):
        store = make_store()
        with self.assertRaises(ValueError):
            remove_product(store, "ORD-0001")
        self.assertEqual("active", store.products["ORD-0001"].status)

    def test_on_closed_order_is_allowed(self):
        store = make_store()
        self.assertEqual("deleted", remove_product(store, "DON-0001"))

    def test_unknown_sku_is_rejected(self):
        with self.assertRaises(ValueError):
            remove_product(make_store(), "ZZZ-9999")

    def test_archived_product_stays_archived(self):
        store = make_store()
        remove_product(store, "PIP-0001")
        self.assertEqual("archived", remove_product(store, "PIP-0001"))

    def test_other_products_untouched(self):
        store = make_store()
        remove_product(store, "NEW-0001")
        self.assertEqual(4, len(store.products))


if __name__ == "__main__":
    unittest.main()
