"""R9 save_data / load_data - white-box: loop testing.

The loops in storage.py go over the items of each collection (saving
and loading) and over the lines of a purchase order (_build). Each loop
is run zero times, once and many times. The loop over COLLECTIONS
always runs 12 times, once for each collection.
"""
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store
from stock_control.models import (
    Category, Movement, OrderLine, Product, PurchaseOrder)
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


def store_with_many_items():
    store = Store()
    store.categories["Tools"] = Category("Tools")
    for number in range(1, 4):
        sku = f"TLS-{number:04d}"
        store.products[sku] = Product(sku, sku, "Tools", 1.0)
        store.movements.append(Movement(f"MV{number:04d}", sku, "receive",
                                        1, "WH1", "2026-11-01"))
    return store


class TestSaveLoadLoopTesting(FileTestCase):

    def round_trip(self, store):
        save_data(store, self.data_file)
        return load_data(self.data_file)

    # Case 1: zero iterations - every collection is empty
    def test_items_zero_iterations(self):
        self.assertEqual(Store(), self.round_trip(Store()))

    # Case 2: one iteration - one item in every collection
    def test_items_one_iteration(self):
        self.assertEqual(make_store(), self.round_trip(make_store()))

    # Case 3: many iterations - three products and three movements
    def test_items_many_iterations(self):
        store = store_with_many_items()
        self.assertEqual(store, self.round_trip(store))

    # Order lines: zero, one and many passes through the loop in _build
    def test_order_lines_zero_one_many(self):
        for count in (0, 1, 3):
            with self.subTest(lines=count):
                store = Store()
                lines = [OrderLine("TLS-0001", n + 1, 2.0)
                         for n in range(count)]
                store.purchase_orders["PO0001"] = PurchaseOrder(
                    "PO0001", "SUP001", lines)
                loaded = self.round_trip(store)
                self.assertEqual(lines, loaded.purchase_orders["PO0001"].lines)


if __name__ == "__main__":
    unittest.main()
