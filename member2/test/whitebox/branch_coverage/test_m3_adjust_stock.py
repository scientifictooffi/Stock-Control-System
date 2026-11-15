import unittest
from member2.test.m3_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, make_store)
from stock_control.movements.adjustments import adjust_stock


class TestAdjustStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_branch_product_true(self):
        with self.assertRaises(KeyError):
            adjust_stock(self.store, UNKNOWN_SKU, -1, "lost", "MAIN", TODAY)

    def test_branch_reason_true(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -1, "theft", "MAIN", TODAY)

    def test_branch_change_true(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, 2.5, "lost", "MAIN", TODAY)

    def test_branch_warehouse_true(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -1, "lost", "SOUTH", TODAY)

    def test_branch_below_zero_true(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -51, "lost", "MAIN", TODAY, "kim")

    def test_branch_approver_true(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -10, "damaged", "MAIN", TODAY,
                         "sam")

    def test_branch_big_change_true(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -10, "damaged", "MAIN", TODAY,
                         "kim"), MAIN_QTY - 10)

    def test_all_branches_false_success(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, 2, "count error", "MAIN", TODAY),
            MAIN_QTY + 2)
        self.assertEqual(self.store.movements[0].reason, "count error")


if __name__ == "__main__":
    unittest.main()
