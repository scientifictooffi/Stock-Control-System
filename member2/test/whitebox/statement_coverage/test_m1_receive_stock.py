import unittest
from member2.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_s1_unknown_product(self):
        with self.assertRaises(KeyError):
            receive_stock(self.store, UNKNOWN_SKU, 5, "MAIN", TODAY)

    def test_s2_inactive_product(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ARCHIVED_SKU, 5, "MAIN", TODAY)

    def test_s3_bad_quantity(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 0, "MAIN", TODAY)

    def test_s4_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "EAST", TODAY)

    def test_s5_bad_date_format(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 5, "MAIN", "2026/11/07")

    def test_s6_use_by_in_the_past(self):
        with self.assertRaises(ValueError):
            receive_stock(
                self.store, ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-01")

    def test_s7_successful_delivery_with_use_by(self):
        result = receive_stock(
            self.store, ACTIVE_SKU, 5, "NORTH", TODAY, "2026-12-01", "alex")
        self.assertEqual(result, START_QTY + 5)
        self.assertEqual(
            self.store.products[ACTIVE_SKU].stock_by_warehouse["NORTH"], 5)
        self.assertEqual(self.store.batches[0].batch_id, "B0001")
        self.assertEqual(self.store.movements[0].reason, "delivery B0001")


if __name__ == "__main__":
    unittest.main()
