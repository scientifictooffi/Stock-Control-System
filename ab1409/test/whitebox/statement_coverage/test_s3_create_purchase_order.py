import unittest
from ab1409.test.s3_fixtures import (
    ACME, BRICK_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, TODAY,
    UNKNOWN_ID, make_store)
from stock_control.purchasing.orders import create_purchase_order


class TestCreatePurchaseOrderStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_statement_raise_unknown_supplier(self):
        with self.assertRaises(KeyError):
            create_purchase_order(
                self.store, UNKNOWN_ID, [(PIPE_SKU, 5)], TODAY)

    def test_statement_raise_supplier_not_active(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, SUSPENDED_ID, [(BRICK_SKU, 5)], TODAY)

    def test_statement_raise_no_items(self):
        with self.assertRaises(ValueError):
            create_purchase_order(self.store, DELTA, [], TODAY)

    def test_statement_raise_bad_date(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, DELTA, [(PIPE_SKU, 1)], "2026-02-30")

    def test_statement_raise_item_not_a_pair(self):
        with self.assertRaises(ValueError):
            create_purchase_order(self.store, DELTA, [PIPE_SKU], TODAY)

    def test_statement_raise_item_not_sold(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, ACME, [(BRICK_SKU, 5)], TODAY)

    def test_statement_raise_quantity(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, DELTA, [(PIPE_SKU, 0)], TODAY)

    def test_statement_raise_duplicate_item(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, DELTA, [(PIPE_SKU, 1), (PIPE_SKU, 1)], TODAY)

    def test_statement_raise_below_minimum(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, ACME, [(PIPE_SKU, 1)], TODAY)

    def test_statements_success_path(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 6), (TAP_SKU, 2)], TODAY)
        self.assertEqual(order.po_id, "PO0001")
        self.assertEqual(order.total_ex_vat, 71.00)
        self.assertEqual(order.total_inc_vat, 85.20)
        self.assertEqual(self.store.purchase_orders["PO0001"], order)


if __name__ == "__main__":
    unittest.main()
