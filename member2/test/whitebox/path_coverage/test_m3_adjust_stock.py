import unittest
from member2.test.m3_fixtures import (
    DEAR_SKU, MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, make_store, snapshot)
from stock_control.movements.adjustments import adjust_stock


class TestAdjustStockPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args):
        with self.assertRaises(error) as ctx:
            adjust_stock(self.store, *args)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def assert_path_adjusted(self, expected, *args):
        self.assertEqual(adjust_stock(self.store, *args), expected)
        self.assertEqual(len(self.store.movements), 1)

    def test_path_1_unknown_product(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, -1, "lost", "MAIN",
            TODAY)

    def test_path_2_invalid_reason(self):
        self.assert_path_refused(
            ValueError, "reason", SKU, -1, "missing", "MAIN", TODAY)

    def test_path_3_invalid_change(self):
        self.assert_path_refused(
            ValueError, "change", SKU, True, "lost", "MAIN", TODAY)

    def test_path_4_unknown_warehouse(self):
        self.assert_path_refused(
            ValueError, "warehouse", SKU, -1, "lost", "EAST", TODAY)

    def test_path_5_below_zero(self):
        self.assert_path_refused(
            ValueError, "below 0", SKU, -1, "lost", "NORTH", TODAY, "kim")

    def test_path_6_success(self):
        self.assert_path_adjusted(
            MAIN_QTY - 3, SKU, -3, "damaged", "MAIN", TODAY)

    def test_path_7_not_approved(self):
        self.assert_path_refused(
            ValueError, "manager approval", DEAR_SKU, -3, "damaged", "MAIN",
            TODAY, "lee")

    def test_path_8_success_approved(self):
        self.assert_path_adjusted(
            97, DEAR_SKU, -3, "damaged", "MAIN", TODAY, "kim")


if __name__ == "__main__":
    unittest.main()
