"""R9 save_data / load_data - white-box: concolic testing.

One test per iteration in docs/research/R9_save_load.md.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.models import Category, OrderLine, PurchaseOrder
from stock_control.reporting.storage import (
    _build, _can_read, backup_path, load_data, save_data)
from stock_control.store import Store


class TestSaveLoadConcolic(FileTestCase):

    def test_iteration_1_no_files(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_iteration_2_good_file(self):
        self.save_good(self.data_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_iteration_3_damaged_file_no_backup(self):
        self.write_text(self.data_file, "{x")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    def test_iteration_4_damaged_file_good_backup(self):
        self.write_text(self.data_file, "{x")
        self.save_good(self.backup_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_iteration_5_not_a_store(self):
        with self.assertRaisesRegex(ValueError, "must be a Store"):
            save_data(None, self.data_file)

    def test_iteration_6_store_no_file(self):
        save_data(make_store(), self.data_file)
        self.assertFalse(os.path.exists(self.backup_file))

    def test_iteration_7_store_good_file(self):
        self.save_good(self.data_file, make_store())
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))

    def test_iteration_8_folder_cannot_be_read(self):
        os.mkdir(self.data_file)
        with self.assertRaisesRegex(ValueError,
                                    r"stock\.json \(file cannot be read"):
            load_data(self.data_file)

    def test_iteration_9_list_not_saved_data(self):
        self.write_text(self.data_file, "[]")
        with self.assertRaisesRegex(ValueError, "does not hold saved data"):
            load_data(self.data_file)

    def test_iteration_10_row_does_not_match(self):
        self.write_text(self.data_file, '{"products": []}')
        with self.assertRaisesRegex(ValueError, "does not hold saved data"):
            load_data(self.data_file)

    def test_iteration_11_empty_object(self):
        self.write_text(self.data_file, "{}")
        self.assertEqual(Store(), load_data(self.data_file))

    def test_iteration_12_can_read(self):
        self.save_good(self.data_file, make_store())
        self.assertTrue(_can_read(self.data_file))
        self.write_text(self.data_file, "{x")
        self.assertFalse(_can_read(self.data_file))

    def test_iteration_13_build(self):
        self.assertEqual(Category("Tools"),
                         _build(Category, {"name": "Tools"}))
        row = {"po_id": "PO1", "supplier_id": "S1",
               "lines": [{"sku": "A", "quantity": 1, "unit_price": 2.0}]}
        self.assertEqual([OrderLine("A", 1, 2.0)],
                         _build(PurchaseOrder, row).lines)

    def test_backup_path_one_run(self):
        self.assertEqual("data/stock.backup.json",
                         backup_path("data/stock.json"))


if __name__ == "__main__":
    unittest.main()
