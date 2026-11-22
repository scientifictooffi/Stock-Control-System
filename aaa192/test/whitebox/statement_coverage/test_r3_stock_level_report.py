"""R3 stock_level_report - white-box: statement coverage.

These tests run every statement in stock_level_report() and
_stock_status() at least once (both raises, both branches of the loop,
the warehouse sort and every return in _stock_status).
"""
import unittest

from aaa192.test.r3_fixtures import make_store, statuses
from stock_control.reporting.reports import stock_level_report


class TestStockLevelReportStatementCoverage(unittest.TestCase):

    def test_statements_bad_group_raise(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), group_by="day")

    def test_statements_bad_category_raise(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), category="Garden")

    def test_statements_product_lines_all_statuses(self):
        result = statuses(stock_level_report(make_store()))
        self.assertEqual({"out", "low", "in stock", "overstocked"},
                         set(result.values()))

    def test_statements_warehouse_lines_and_sort(self):
        lines = stock_level_report(make_store(), group_by="warehouse")
        keys = [(line["warehouse"], line["sku"]) for line in lines]
        self.assertEqual(sorted(keys), keys)


if __name__ == "__main__":
    unittest.main()
