"""R3 stock_level_report - white-box: path coverage.

Paths through stock_level_report():
P1 D1=T -> "cannot group by"
P2 D1=F D2=T -> "category does not exist"
P3 D1=F D2=F, no product passes the filter -> []
P4 D1=F D2=F, group_by product -> product lines
P5 D1=F D2=F, group_by warehouse -> warehouse lines, sorted
Paths through _stock_status() (cyclomatic complexity 4):
Q1 S1=T -> out   Q2 S2=T -> low   Q3 S3=T -> overstocked
Q4 all False -> in stock
"""
import unittest

from member4.test.r3_fixtures import make_product, make_store
from stock_control.models import Category
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store


def one_product_status(quantity, min_level, max_level):
    store = Store()
    store.categories["Tools"] = Category("Tools")
    store.products["TLS-0001"] = make_product(
        "TLS-0001", quantity, min_level, max_level)
    return stock_level_report(store)[0]["status"]


class TestStockLevelReportPathCoverage(unittest.TestCase):

    def test_path_p1_bad_group(self):
        with self.assertRaisesRegex(ValueError, "cannot group by"):
            stock_level_report(make_store(), group_by="day")

    def test_path_p2_bad_category(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            stock_level_report(make_store(), category="Garden")

    def test_path_p3_no_lines(self):
        self.assertEqual([], stock_level_report(Store()))

    def test_path_p4_product_lines(self):
        lines = stock_level_report(make_store())
        self.assertEqual("TLS-0003", lines[-1]["sku"])

    def test_path_p5_warehouse_lines(self):
        lines = stock_level_report(make_store(), group_by="warehouse")
        self.assertEqual(("WH2", "TLS-0003"),
                         (lines[-1]["warehouse"], lines[-1]["sku"]))

    def test_path_q1_out(self):
        self.assertEqual("out", one_product_status(0, 5, 50))

    def test_path_q2_low(self):
        self.assertEqual("low", one_product_status(2, 5, 50))

    def test_path_q3_overstocked(self):
        self.assertEqual("overstocked", one_product_status(70, 5, 50))

    def test_path_q4_in_stock(self):
        self.assertEqual("in stock", one_product_status(30, 5, 50))


if __name__ == "__main__":
    unittest.main()
