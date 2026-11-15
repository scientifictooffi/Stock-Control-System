import unittest
from member2.test.m2_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, batch, make_store)
from stock_control.movements.issuing import issue_stock

class TestIssueStockStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_statement_raise_unknown_product(self):
        with self.assertRaises(KeyError):
            issue_stock(self.store, UNKNOWN_SKU, 1, "MAIN", TODAY)

    def test_statement_raise_quantity(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 0, "MAIN", TODAY)

    def test_statement_raise_warehouse(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "EAST", TODAY)

    def test_statement_raise_not_enough_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 11, "MAIN", TODAY)

    def test_statement_raise_no_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 1, "NORTH", TODAY, True)

    def test_statement_part_order_unbatched_stock(self):
        self.assertEqual(
            issue_stock(self.store, SKU, 15, "MAIN", TODAY, True), MAIN_QTY)
        self.assertIn("no batch:1", self.store.movements[0].reason)

    def test_statements_success_path(self):
        self.assertEqual(issue_stock(self.store, SKU, 5, "MAIN", TODAY), 5)
        self.assertEqual(batch(self.store, "B0003").quantity, 2)


if __name__ == "__main__":
    unittest.main()
