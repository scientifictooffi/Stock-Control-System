import unittest
from bpt5.test.m3_fixtures import (
    DEAR_SKU, MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, make_store, snapshot)
from stock_control.movements.adjustments import adjust_stock


class TestAdjustStockEquivalencePartitioning(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args):
        with self.assertRaises(error):
            adjust_stock(self.store, *args)
        self.assertEqual(self.store, self.before)

    def test_valid_class_all_rules_pass(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -2, "damaged", "MAIN", TODAY),
            MAIN_QTY - 2)
        self.assertEqual(self.store.products[SKU].quantity, MAIN_QTY - 2)

    def test_valid_class_lost(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -1, "lost", "MAIN", TODAY),
            MAIN_QTY - 1)

    def test_valid_class_count_error_adds_stock(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, 3, "count error", "MAIN", TODAY),
            MAIN_QTY + 3)

    def test_valid_class_big_change_approved(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -20, "lost", "MAIN", TODAY, "kim"),
            MAIN_QTY - 20)

    def test_valid_class_saved_in_history(self):
        adjust_stock(self.store, SKU, -20, "damaged", "MAIN", TODAY, "kim",
                     "alex")
        movement = self.store.movements[-1]
        self.assertEqual(
            (movement.sku, movement.movement_type, movement.quantity,
             movement.warehouse, movement.date, movement.user,
             movement.reason),
            (SKU, "adjust", -20, "MAIN", TODAY, "alex",
             "damaged, approved by kim"))

    def test_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, -1, "lost", "MAIN", TODAY)

    def test_invalid_reason_stolen(self):
        self.assert_refused(ValueError, SKU, -1, "stolen", "MAIN", TODAY)

    def test_empty_reason(self):
        self.assert_refused(ValueError, SKU, -1, "", "MAIN", TODAY)

    def test_change_zero(self):
        self.assert_refused(ValueError, SKU, 0, "lost", "MAIN", TODAY)

    def test_change_not_whole_number(self):
        self.assert_refused(ValueError, SKU, -1.5, "lost", "MAIN", TODAY)

    def test_change_not_int(self):
        self.assert_refused(ValueError, SKU, True, "count error", "MAIN",
                            TODAY)

    def test_unknown_warehouse(self):
        self.assert_refused(ValueError, SKU, -1, "lost", "EAST", TODAY)

    def test_stock_below_zero(self):
        self.assert_refused(ValueError, SKU, -51, "lost", "MAIN", TODAY,
                            "kim")

    def test_big_change_not_approved(self):
        self.assert_refused(ValueError, SKU, -20, "lost", "MAIN", TODAY)

    def test_big_value_not_approved(self):
        self.assert_refused(ValueError, DEAR_SKU, -3, "damaged", "MAIN",
                            TODAY)

    def test_approver_not_manager(self):
        self.assert_refused(ValueError, SKU, -20, "lost", "MAIN", TODAY,
                            "sam")

    def test_approver_inactive(self):
        self.assert_refused(ValueError, SKU, -20, "lost", "MAIN", TODAY,
                            "lee")

    def test_unknown_approver(self):
        self.assert_refused(ValueError, SKU, -20, "lost", "MAIN", TODAY,
                            "bob")


if __name__ == "__main__":
    unittest.main()
