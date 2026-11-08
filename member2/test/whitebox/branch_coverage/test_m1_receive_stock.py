import unittest
from member2.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_b1_d1_true_unknown_product(self):
        with self.assertRaises(KeyError):
            receive_stock(self.store, UNKNOWN_SKU, 5, "MAIN", TODAY)

    def test_b2_d2_true_inactive_product(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ARCHIVED_SKU, 5, "MAIN", TODAY)

    def test_b3_d3_true_bad_quantity(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, -3, "MAIN", TODAY)

    def test_b4_d4_true_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "SOUTH", TODAY)

    def test_b5_d5_true_bad_date(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", "2026-11-31")

    def test_b6_d6_false_no_use_by(self):
        self.assertEqual(
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", TODAY),
            START_QTY + 5)
        self.assertIsNone(self.store.batches[0].use_by_date)

    def test_b7_d7_true_bad_use_by(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "soon")

    def test_b8_d8_true_use_by_in_the_past(self):
        with self.assertRaises(ValueError):
            receive_stock(
                self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-06")

    def test_b9_d8_false_use_by_on_or_after_date(self):
        self.assertEqual(
            receive_stock(
                self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-20"),
            START_QTY + 5)
        self.assertEqual(
            self.store.products[ACTIVE_SKU].stock_by_warehouse["MAIN"],
            START_QTY + 5)


if __name__ == "__main__":
    unittest.main()
