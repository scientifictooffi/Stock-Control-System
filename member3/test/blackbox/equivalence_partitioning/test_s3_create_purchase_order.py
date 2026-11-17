import unittest
from member3.test.s3_fixtures import (
    ACME, BRICK_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, TODAY,
    UNKNOWN_ID, UNKNOWN_SKU, make_store, snapshot)
from stock_control.purchasing.orders import create_purchase_order


class TestCreatePurchaseOrderValidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_valid_class_one_item(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 6)], TODAY)
        self.assertEqual(order.po_id, "PO0001")
        self.assertEqual(order.supplier_id, ACME)
        self.assertEqual(order.status, "draft")
        self.assertEqual(order.created_date, TODAY)
        self.assertEqual(
            [(x.sku, x.quantity, x.unit_price, x.received)
             for x in order.lines],
            [(PIPE_SKU, 6, 10.00, 0)])
        self.assertIs(self.store.purchase_orders["PO0001"], order)

    def test_valid_class_two_items_with_vat(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 6), (TAP_SKU, 2)], TODAY)
        self.assertEqual(order.total_ex_vat, 71.00)
        self.assertEqual(order.total_inc_vat, 85.20)

    def test_valid_class_vat_rounded_to_the_penny(self):
        order = create_purchase_order(
            self.store, DELTA, [(BRICK_SKU, 3)], TODAY)
        self.assertEqual(order.total_ex_vat, 9.99)
        self.assertEqual(order.total_inc_vat, 11.99)

    def test_valid_class_supplier_without_minimum(self):
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(order.total_inc_vat, 14.40)

    def test_valid_class_items_given_as_lists(self):
        order = create_purchase_order(
            self.store, DELTA, [[PIPE_SKU, 2], [BRICK_SKU, 10]], TODAY)
        self.assertEqual(len(order.lines), 2)

    def test_valid_class_second_order_gets_next_id(self):
        create_purchase_order(self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(order.po_id, "PO0002")
        self.assertEqual(len(self.store.purchase_orders), 2)

    def test_valid_class_each_supplier_uses_its_own_price(self):
        acme = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 5)], TODAY)
        delta = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 5)], TODAY)
        self.assertEqual(acme.lines[0].unit_price, 10.00)
        self.assertEqual(delta.lines[0].unit_price, 12.00)


class TestCreatePurchaseOrderInvalidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args):
        with self.assertRaises(error):
            create_purchase_order(self.store, *args)
        self.assertEqual(self.store, self.before)

    def test_unknown_supplier(self):
        self.assert_refused(KeyError, UNKNOWN_ID, [(PIPE_SKU, 5)], TODAY)

    def test_suspended_supplier(self):
        self.assert_refused(
            ValueError, SUSPENDED_ID, [(BRICK_SKU, 500)], TODAY)

    def test_no_items_empty_list(self):
        self.assert_refused(ValueError, DELTA, [], TODAY)

    def test_no_items_none(self):
        self.assert_refused(ValueError, DELTA, None, TODAY)

    def test_item_not_sold_by_this_supplier(self):
        self.assert_refused(ValueError, ACME, [(BRICK_SKU, 100)], TODAY)

    def test_item_not_sold_by_anyone(self):
        self.assert_refused(ValueError, ACME, [(UNKNOWN_SKU, 100)], TODAY)

    def test_one_good_item_and_one_not_sold(self):
        self.assert_refused(
            ValueError, ACME, [(PIPE_SKU, 10), (BRICK_SKU, 1)], TODAY)

    def test_quantity_zero(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 0)], TODAY)

    def test_quantity_negative(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, -4)], TODAY)

    def test_quantity_not_whole_number(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 2.5)], TODAY)

    def test_quantity_is_text(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, "3")], TODAY)

    def test_quantity_is_bool(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, True)], TODAY)

    def test_same_item_twice(self):
        self.assert_refused(
            ValueError, DELTA, [(PIPE_SKU, 1), (PIPE_SKU, 2)], TODAY)

    def test_item_is_not_a_pair(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 1, 9.99)], TODAY)
        self.assert_refused(ValueError, DELTA, [PIPE_SKU], TODAY)

    def test_below_minimum_order(self):
        self.assert_refused(ValueError, ACME, [(PIPE_SKU, 4)], TODAY)

    def test_date_wrong_format(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 1)], "07/11/2026")

    def test_date_compact_format(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 1)], "20261107")

    def test_date_missing(self):
        self.assert_refused(ValueError, DELTA, [(PIPE_SKU, 1)], None)


if __name__ == "__main__":
    unittest.main()
