import unittest
from member2.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store,
    snapshot)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockValidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_v1_v2_v3_v4_v5_valid_delivery_without_use_by(self):
        result = receive_stock(self.store, ACTIVE_SKU, 10, "MAIN", TODAY)
        self.assertEqual(result, START_QTY + 10)

    def test_v6_valid_delivery_with_future_use_by(self):
        result = receive_stock(
            self.store, ACTIVE_SKU, 10, "NORTH", TODAY, "2027-03-01")
        self.assertEqual(result, START_QTY + 10)
        self.assertEqual(self.store.batches[-1].use_by_date, "2027-03-01")

    def test_valid_delivery_updates_stock_and_history(self):
        receive_stock(self.store, ACTIVE_SKU, 6, "NORTH", TODAY, user="alex")
        product = self.store.products[ACTIVE_SKU]
        self.assertEqual(product.stock_by_warehouse,
                         {"MAIN": START_QTY, "NORTH": 6})
        self.assertEqual(len(self.store.batches), 1)
        movement = self.store.movements[-1]
        self.assertEqual(
            (movement.sku, movement.movement_type, movement.quantity,
             movement.warehouse, movement.user),
            (ACTIVE_SKU, "receive", 6, "NORTH", "alex"))


class TestReceiveStockInvalidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args):
        with self.assertRaises(error):
            receive_stock(self.store, *args)
        self.assertEqual(self.store, self.before)

    def test_i1_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, 10, "MAIN", TODAY)

    def test_i2_archived_product(self):
        self.assert_refused(ValueError, ARCHIVED_SKU, 10, "MAIN", TODAY)

    def test_i3_quantity_not_positive(self):
        self.assert_refused(ValueError, ACTIVE_SKU, -5, "MAIN", TODAY)

    def test_i4_quantity_not_whole_number(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 2.5, "MAIN", TODAY)

    def test_i5_unknown_warehouse(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "EAST", TODAY)

    def test_i6_date_wrong_format(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "MAIN", "07/11/2026")

    def test_i6_date_compact_iso_form_refused(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "MAIN", "20261107")

    def test_i7_use_by_in_the_past(self):
        self.assert_refused(
            ValueError, ACTIVE_SKU, 10, "MAIN", TODAY, "2026-10-01")

    def test_i8_use_by_wrong_format(self):
        self.assert_refused(
            ValueError, ACTIVE_SKU, 10, "MAIN", TODAY, "next week")


if __name__ == "__main__":
    unittest.main()
