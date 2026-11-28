"""R9 save_data / load_data - black-box: boundary value analysis.

Tests at the edges: 0, 1 and 2 items, an empty file, the smallest saved
file, and 1 and 2 saves.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.models import Category, OrderLine, Product, PurchaseOrder
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


def store_with_products(count):
    store = Store()
    store.categories["Tools"] = Category("Tools")
    for number in range(1, count + 1):
        sku = f"TLS-{number:04d}"
        store.products[sku] = Product(sku, sku, "Tools", 1.0)
    return store


def store_with_order_lines(count):
    store = Store()
    lines = [OrderLine("TLS-0001", number, 2.0) for number in range(count)]
    store.purchase_orders["PO0001"] = PurchaseOrder("PO0001", "SUP001",
                                                    lines)
    return store


class TestSaveLoadBoundaryValues(FileTestCase):

    def round_trip(self, store):
        save_data(store, self.data_file)
        return load_data(self.data_file)

    def test_products_0_1_2(self):
        for count in (0, 1, 2):
            with self.subTest(products=count):
                store = store_with_products(count)
                loaded = self.round_trip(store)
                self.assertEqual(store, loaded)
                self.assertEqual(count, len(loaded.products))

    def test_order_lines_0_1_2(self):
        for count in (0, 1, 2):
            with self.subTest(lines=count):
                loaded = self.round_trip(store_with_order_lines(count))
                lines = loaded.purchase_orders["PO0001"].lines
                self.assertEqual(count, len(lines))
                self.assertTrue(all(isinstance(line, OrderLine)
                                    for line in lines))

    def test_empty_file_0_bytes_loads_backup(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_smallest_saved_data_2_bytes(self):
        self.write_text(self.data_file, "{}")
        self.assertEqual(Store(), load_data(self.data_file))

    def test_one_character_short_loads_backup(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "{")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_json_list_instead_of_object_fails(self):
        self.write_text(self.data_file, "[]")
        with self.assertRaisesRegex(ValueError, "does not hold saved data"):
            load_data(self.data_file)

    def test_one_save_no_backup_yet(self):
        save_data(make_store(), self.data_file)
        self.assertFalse(os.path.exists(self.backup_file))

    def test_two_saves_first_is_backup(self):
        save_data(make_store(), self.data_file)
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))


if __name__ == "__main__":
    unittest.main()
