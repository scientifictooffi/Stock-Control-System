import unittest
from bpt5.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_branch_product_true(self):
        with self.assertRaises(KeyError):
            receive_stock(self.store, UNKNOWN_SKU, 5, "MAIN", TODAY)

    def test_branch_not_active_true(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ARCHIVED_SKU, 5, "MAIN", TODAY)

    def test_branch_quantity_true(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, -3, "MAIN", TODAY)

    def test_branch_warehouse_true(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "SOUTH", TODAY)

    def test_branch_date_true(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", "2026-11-31")

    def test_branch_no_use_by_success(self):
        self.assertEqual(
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", TODAY),
            START_QTY + 5)
        self.assertIsNone(self.store.batches[0].use_by_date)

    def test_branch_use_by_format_true(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "soon")

    def test_branch_use_by_past_true(self):
        with self.assertRaises(ValueError):
            receive_stock(
                self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-06")

    def test_all_branches_false_success(self):
        self.assertEqual(
            receive_stock(
                self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-20"),
            START_QTY + 5)
        self.assertEqual(
            self.store.products[ACTIVE_SKU].stock_by_warehouse["MAIN"],
            START_QTY + 5)


if __name__ == "__main__":
    unittest.main()
