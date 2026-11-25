import unittest
from ab1409.test.s3_fixtures import (
    ACME, BRICK_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, TODAY,
    UNKNOWN_ID, UNKNOWN_SKU, make_store)
from stock_control.purchasing.orders import create_purchase_order


class TestCreatePurchaseOrderBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def refused(self, error, supplier, lines, day=TODAY):
        with self.assertRaises(error):
            create_purchase_order(self.store, supplier, lines, day)

    def test_branch_supplier_missing_true(self):
        self.refused(KeyError, UNKNOWN_ID, [(PIPE_SKU, 1)])

    def test_branch_supplier_not_active_true(self):
        self.refused(ValueError, SUSPENDED_ID, [(BRICK_SKU, 1)])

    def test_branch_no_lines_true_empty(self):
        self.refused(ValueError, DELTA, [])

    def test_branch_no_lines_true_none(self):
        self.refused(ValueError, DELTA, None)

    def test_branch_date_invalid_true_not_text(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, 1)], 20261107)

    def test_branch_date_invalid_true_not_a_date(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, 1)], "2026-11-31")

    def test_branch_date_invalid_true_not_round_trip(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, 1)], "20261107")

    def test_branch_item_not_tuple_or_list_true(self):
        self.refused(ValueError, DELTA, ["PIP-0001"])

    def test_branch_item_wrong_length_true(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU,)])

    def test_branch_sku_not_sold_true(self):
        self.refused(ValueError, ACME, [(UNKNOWN_SKU, 5)])

    def test_branch_quantity_not_int_true(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, 1.0)])

    def test_branch_quantity_bool_true(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, True)])

    def test_branch_quantity_not_positive_true(self):
        self.refused(ValueError, DELTA, [(PIPE_SKU, -2)])

    def test_branch_duplicate_sku_true(self):
        self.refused(ValueError, DELTA, [(BRICK_SKU, 1), (BRICK_SKU, 2)])

    def test_branch_below_minimum_true(self):
        self.refused(ValueError, ACME, [(TAP_SKU, 9)])

    def test_branch_all_false_one_item_success(self):
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(order.total_inc_vat, 14.40)

    def test_branch_loop_runs_more_than_once_success(self):
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1), (BRICK_SKU, 3)], TODAY)
        self.assertEqual(order.total_ex_vat, 21.99)
        self.assertEqual(order.total_inc_vat, 26.39)

    def test_branch_total_equal_to_minimum_false(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 5)], TODAY)
        self.assertEqual(order.total_ex_vat, 50.00)


if __name__ == "__main__":
    unittest.main()
