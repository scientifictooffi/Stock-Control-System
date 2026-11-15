import unittest
from member2.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store,
    snapshot)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockValidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_valid_class_all_rules_pass(self):
        result = receive_stock(self.store, ACTIVE_SKU, 10, "MAIN", TODAY)
        self.assertEqual(result, START_QTY + 10)

    def test_valid_class_future_use_by(self):
        result = receive_stock(
            self.store, ACTIVE_SKU, 10, "NORTH", TODAY, "2027-03-01")
        self.assertEqual(result, START_QTY + 10)
        self.assertEqual(self.store.batches[-1].use_by_date, "2027-03-01")

    def test_valid_class_saved_in_history(self):
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

    def test_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, 10, "MAIN", TODAY)

    def test_archived_product(self):
        self.assert_refused(ValueError, ARCHIVED_SKU, 10, "MAIN", TODAY)

    def test_quantity_not_positive(self):
        self.assert_refused(ValueError, ACTIVE_SKU, -5, "MAIN", TODAY)

    def test_quantity_not_whole_number(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 2.5, "MAIN", TODAY)

    def test_unknown_warehouse(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "EAST", TODAY)

    def test_date_wrong_format(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "MAIN", "07/11/2026")

    def test_date_compact_format(self):
        self.assert_refused(ValueError, ACTIVE_SKU, 10, "MAIN", "20261107")

    def test_use_by_in_the_past(self):
        self.assert_refused(
            ValueError, ACTIVE_SKU, 10, "MAIN", TODAY, "2026-10-01")

    def test_use_by_wrong_format(self):
        self.assert_refused(
            ValueError, ACTIVE_SKU, 10, "MAIN", TODAY, "next week")


if __name__ == "__main__":
    unittest.main()
