"""R9 save_data / load_data - white-box: symbolic execution.

One test per leaf of the trees in docs/research/R9_save_load.md.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.models import Category, OrderLine, PurchaseOrder
from stock_control.reporting.storage import (
    _build, _can_read, backup_path, load_data, save_data)
from stock_control.store import Store


class TestSaveLoadSymbolicExecution(FileTestCase):

    def test_leaf_s1(self):
        with self.assertRaisesRegex(ValueError, "must be a Store"):
            save_data({}, self.data_file)

    def test_leaf_s2(self):
        self.save_good(self.data_file, make_store())
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_leaf_s3(self):
        self.save_good(self.backup_file, other_store())
        self.write_text(self.data_file, "{x")
        save_data(make_store(), self.data_file)
        self.assertEqual(other_store(), load_data(self.backup_file))
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_leaf_l1(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_leaf_l2(self):
        self.save_good(self.data_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_leaf_l3(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "{x")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_leaf_l4(self):
        self.write_text(self.data_file, "{x")
        self.assertFalse(os.path.exists(self.backup_file))
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    def assert_data_file_problem(self, problem):
        with self.assertRaisesRegex(ValueError,
                                    r"stock\.json \(file " + problem):
            load_data(self.data_file)

    def test_leaf_r1(self):
        os.mkdir(self.data_file)
        self.assert_data_file_problem("cannot be read")

    def test_leaf_r2(self):
        self.write_text(self.data_file, "{x")
        self.assert_data_file_problem("is not valid JSON")

    def test_leaf_r3(self):
        self.write_text(self.data_file, "[]")
        self.assert_data_file_problem("does not hold saved data")

    def test_leaf_r4(self):
        self.write_text(self.data_file, '{"products": []}')
        self.assert_data_file_problem("does not hold saved data")

    def test_leaf_r5(self):
        self.write_text(self.data_file, "{}")
        self.assertEqual(Store(), load_data(self.data_file))

    def test_leaf_c1(self):
        self.write_text(self.data_file, "{x")
        self.assertFalse(_can_read(self.data_file))

    def test_leaf_c2(self):
        self.save_good(self.data_file, make_store())
        self.assertTrue(_can_read(self.data_file))

    def test_leaf_b1(self):
        row = {"po_id": "PO1", "supplier_id": "S1",
               "lines": [{"sku": "A", "quantity": 1, "unit_price": 2.0}]}
        order = _build(PurchaseOrder, row)
        self.assertEqual([OrderLine("A", 1, 2.0)], order.lines)

    def test_leaf_b2(self):
        self.assertEqual(Category("Tools"),
                         _build(Category, {"name": "Tools"}))

    def test_backup_path(self):
        self.assertEqual("data/stock.backup.json",
                         backup_path("data/stock.json"))


if __name__ == "__main__":
    unittest.main()
