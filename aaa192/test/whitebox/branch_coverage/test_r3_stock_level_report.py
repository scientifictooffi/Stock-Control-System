"""R3 stock_level_report - white-box: branch coverage.

Decisions:
D1 group_by not in GROUP_OPTIONS
D2 category is not None and category not in store.categories
D3 product is not archived and matches the category (filter)
D4 group_by == "product" (inside the loop)
D5 group_by == "warehouse" (sort after the loop)
S1 quantity <= 0   S2 quantity < min_level
S3 max_level > 0 and quantity > max_level
Each decision is made True once and False once.
"""
import unittest

from aaa192.test.r3_fixtures import make_product, make_store, statuses
from stock_control.models import Category
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store


class TestStockLevelReportBranchCoverage(unittest.TestCase):

    def test_d1_true(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), group_by="day")

    def test_d2_true(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), category="Garden")

    def test_d2_false_with_category_d3_true_and_false(self):
        lines = stock_level_report(make_store(), category="Tools")
        self.assertEqual(["TLS-0001", "TLS-0002", "TLS-0003"],
                         [line["sku"] for line in lines])

    def test_d4_true_d5_false(self):
        lines = stock_level_report(make_store())
        self.assertNotIn("warehouse", lines[0])

    def test_d4_false_d5_true(self):
        lines = stock_level_report(make_store(), group_by="warehouse")
        self.assertEqual("WH1", lines[0]["warehouse"])

    def test_s1_s2_s3_true_and_false(self):
        result = statuses(stock_level_report(make_store()))
        self.assertEqual("out", result["TLS-0001"])
        self.assertEqual("low", result["TLS-0002"])
        self.assertEqual("overstocked", result["PNT-0001"])
        self.assertEqual("in stock", result["TLS-0003"])

    def test_s3_false_because_no_maximum(self):
        store = Store()
        store.categories["Tools"] = Category("Tools")
        store.products["TLS-0001"] = make_product("TLS-0001", 500, 0, 0)
        self.assertEqual("in stock", stock_level_report(store)[0]["status"])


if __name__ == "__main__":
    unittest.main()
