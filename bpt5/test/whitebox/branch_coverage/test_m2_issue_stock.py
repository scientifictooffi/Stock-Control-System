import unittest
from bpt5.test.m2_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, batch, make_store)
from stock_control.movements.issuing import issue_stock


class TestIssueStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_branch_product_true(self):
        with self.assertRaises(KeyError):
            issue_stock(self.store, UNKNOWN_SKU, 1, "MAIN", TODAY)

    def test_branch_quantity_true(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, -1, "MAIN", TODAY)

    def test_branch_warehouse_true(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "SOUTH", TODAY)

    def test_branch_not_enough_stock_true(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 11, "MAIN", TODAY)

    def test_branch_no_stock_true(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "NORTH", TODAY, True)

    def test_branch_unbatched_stock_true(self):
        self.assertEqual(
            issue_stock(self.store, SKU, 12, "MAIN", TODAY, True), MAIN_QTY)
        self.assertEqual(self.store.products[SKU].quantity, 0)

    def test_branch_enough_taken_true(self):
        self.assertEqual(issue_stock(self.store, SKU, 5, "MAIN", TODAY), 5)
        self.assertEqual(batch(self.store, "B0001").quantity, 2)

    def test_all_branches_false_success(self):
        self.assertEqual(issue_stock(self.store, SKU, 9, "MAIN", TODAY), 9)
        self.assertEqual(batch(self.store, "B0003").quantity, 0)

    def test_branch_no_batches(self):
        self.store.batches = []
        self.assertEqual(issue_stock(self.store, SKU, 2, "MAIN", TODAY), 2)
        self.assertEqual(self.store.movements[0].reason,
                         "issued from no batch:2")


if __name__ == "__main__":
    unittest.main()
