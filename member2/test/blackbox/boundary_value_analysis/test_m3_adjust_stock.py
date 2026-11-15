import unittest
from member2.test.m3_fixtures import (
    DEAR_SKU, MAIN_QTY, SKU, TODAY, make_store)
from stock_control.movements.adjustments import adjust_stock


class TestAdjustStockBoundaryValues(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_change_exactly_10_percent_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -5, "lost", "MAIN", TODAY),
            MAIN_QTY - 5)

    def test_change_just_above_10_percent_is_rejected(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -6, "lost", "MAIN", TODAY)

    def test_change_just_below_10_percent_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, 4, "count error", "MAIN", TODAY),
            MAIN_QTY + 4)

    def test_change_in_empty_warehouse_is_rejected(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, 1, "count error", "NORTH", TODAY)

    def test_value_just_below_500_is_accepted(self):
        self.store.products[DEAR_SKU].cost = 249.995
        self.assertEqual(
            adjust_stock(self.store, DEAR_SKU, -2, "damaged", "MAIN", TODAY),
            98)

    def test_value_exactly_500_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, DEAR_SKU, -2, "damaged", "MAIN", TODAY),
            98)

    def test_value_just_above_500_is_rejected(self):
        self.store.products[DEAR_SKU].cost = 250.005
        with self.assertRaises(ValueError):
            adjust_stock(self.store, DEAR_SKU, -2, "damaged", "MAIN", TODAY)

    def test_stock_down_to_zero_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -MAIN_QTY, "lost", "MAIN", TODAY,
                         "kim"), 0)

    def test_stock_down_to_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -MAIN_QTY - 1, "lost", "MAIN",
                         TODAY, "kim")

    def test_change_minus_one_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -1, "lost", "MAIN", TODAY),
            MAIN_QTY - 1)

    def test_change_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, 0, "lost", "MAIN", TODAY)

    def test_change_plus_one_is_accepted(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, 1, "count error", "MAIN", TODAY),
            MAIN_QTY + 1)


if __name__ == "__main__":
    unittest.main()
