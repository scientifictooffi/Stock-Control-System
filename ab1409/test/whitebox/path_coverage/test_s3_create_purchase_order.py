import unittest
from ab1409.test.s3_fixtures import (
    ACME, BRICK_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, TODAY,
    UNKNOWN_ID, make_store, snapshot)
from stock_control.purchasing.orders import create_purchase_order


class TestCreatePurchaseOrderPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_path_refused(
            self, error, message, supplier, lines, day=TODAY):
        with self.assertRaises(error) as ctx:
            create_purchase_order(self.store, supplier, lines, day)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def test_path_1_unknown_supplier(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_ID, [(PIPE_SKU, 1)])

    def test_path_2_supplier_not_active(self):
        self.assert_path_refused(
            ValueError, "not active", SUSPENDED_ID, [(BRICK_SKU, 1)])

    def test_path_3_no_items(self):
        self.assert_path_refused(ValueError, "at least one item", DELTA, [])

    def test_path_4_bad_date(self):
        self.assert_path_refused(
            ValueError, "date must be", DELTA, [(PIPE_SKU, 1)], "7/11/26")

    def test_path_5_first_item_not_a_pair(self):
        self.assert_path_refused(
            ValueError, "(sku, quantity) pair", DELTA, ["PIP-0001"])

    def test_path_6_first_item_not_sold(self):
        self.assert_path_refused(
            ValueError, "not sold by", ACME, [(BRICK_SKU, 1)])

    def test_path_7_first_item_bad_quantity(self):
        self.assert_path_refused(
            ValueError, "quantity", DELTA, [(PIPE_SKU, 0)])

    def test_path_8_one_item_below_minimum(self):
        self.assert_path_refused(
            ValueError, "minimum order", ACME, [(PIPE_SKU, 4)])

    def test_path_9_one_item_success(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 5)], TODAY)
        self.assertEqual(len(order.lines), 1)
        self.assertEqual(order.total_inc_vat, 60.00)

    def test_path_10_second_item_not_a_pair(self):
        self.assert_path_refused(
            ValueError, "(sku, quantity) pair", ACME,
            [(PIPE_SKU, 6), (TAP_SKU, 2, 1)])

    def test_path_11_second_item_not_sold(self):
        self.assert_path_refused(
            ValueError, "not sold by", ACME, [(PIPE_SKU, 6), (BRICK_SKU, 1)])

    def test_path_12_second_item_bad_quantity(self):
        self.assert_path_refused(
            ValueError, "quantity", ACME, [(PIPE_SKU, 6), (TAP_SKU, -1)])

    def test_path_13_second_item_duplicate(self):
        self.assert_path_refused(
            ValueError, "more than once", ACME,
            [(PIPE_SKU, 6), (PIPE_SKU, 1)])

    def test_path_14_two_items_below_minimum(self):
        self.assert_path_refused(
            ValueError, "minimum order", ACME,
            [(PIPE_SKU, 1), (TAP_SKU, 1)])

    def test_path_15_two_items_success(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 6), (TAP_SKU, 2)], TODAY)
        self.assertEqual(len(order.lines), 2)
        self.assertEqual(order.total_inc_vat, 85.20)

    def test_path_16_two_items_no_minimum_success(self):
        order = create_purchase_order(
            self.store, DELTA,
            [(PIPE_SKU, 1), (BRICK_SKU, 1)], TODAY)
        self.assertEqual(len(order.lines), 2)
        self.assertEqual(self.store.purchase_orders["PO0001"], order)


if __name__ == "__main__":
    unittest.main()
