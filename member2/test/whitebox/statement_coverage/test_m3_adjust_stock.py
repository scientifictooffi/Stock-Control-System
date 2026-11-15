import unittest
from member2.test.m3_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, make_store)
from stock_control.movements.adjustments import adjust_stock


class TestAdjustStockStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_statement_raise_unknown_product(self):
        with self.assertRaises(KeyError):
            adjust_stock(self.store, UNKNOWN_SKU, -1, "lost", "MAIN", TODAY)

    def test_statement_raise_reason(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -1, "broken", "MAIN", TODAY)

    def test_statement_raise_change(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, 0, "lost", "MAIN", TODAY)

    def test_statement_raise_warehouse(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -1, "lost", "EAST", TODAY)

    def test_statement_raise_below_zero(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -60, "lost", "MAIN", TODAY)

    def test_statement_raise_needs_approval(self):
        with self.assertRaises(ValueError):
            adjust_stock(self.store, SKU, -20, "lost", "MAIN", TODAY)

    def test_statements_success_path(self):
        self.assertEqual(
            adjust_stock(self.store, SKU, -20, "lost", "MAIN", TODAY, "kim"),
            MAIN_QTY - 20)
        self.assertEqual(self.store.movements[0].reason,
                         "lost, approved by kim")


if __name__ == "__main__":
    unittest.main()
