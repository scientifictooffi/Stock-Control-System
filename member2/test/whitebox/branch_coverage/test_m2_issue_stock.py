import unittest
from member2.test.m2_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, batch, make_store)
from stock_control.movements.issuing import issue_stock


class TestIssueStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_b1_d1_true_unknown_product(self):
        with self.assertRaises(KeyError):
            issue_stock(self.store, UNKNOWN_SKU, 1, "MAIN", TODAY)

    def test_b2_d2_true_bad_quantity(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, -1, "MAIN", TODAY)

    def test_b3_d3_true_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "SOUTH", TODAY)

    def test_b4_d4_true_d5_true_not_enough_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 11, "MAIN", TODAY)

    def test_b5_d5_false_d6_true_no_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "NORTH", TODAY, True)

    def test_b6_d6_false_d9_true_part_order(self):
        self.assertEqual(
            issue_stock(self.store, SKU, 12, "MAIN", TODAY, True), MAIN_QTY)
        self.assertEqual(self.store.products[SKU].quantity, 0)

    def test_b7_d4_false_d8_true_break_d9_false(self):
        self.assertEqual(issue_stock(self.store, SKU, 5, "MAIN", TODAY), 5)
        self.assertEqual(batch(self.store, "B0001").quantity, 2)

    def test_b8_d7_false_loop_ends_d9_false(self):
        self.assertEqual(issue_stock(self.store, SKU, 9, "MAIN", TODAY), 9)
        self.assertEqual(batch(self.store, "B0003").quantity, 0)

    def test_b9_d7_false_no_batches(self):
        self.store.batches = []
        self.assertEqual(issue_stock(self.store, SKU, 2, "MAIN", TODAY), 2)
        self.assertEqual(self.store.movements[0].reason,
                         "issued from no batch:2")

if __name__ == "__main__":
    unittest.main()
