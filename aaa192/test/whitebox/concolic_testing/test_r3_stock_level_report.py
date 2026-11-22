"""R3 stock_level_report - white-box: concolic testing.

Start from one concrete input, record the path it takes, negate the last
decision on that path, solve for a new input and repeat (see
docs/research/R3_stock_level_report.md for each iteration).
"""
import unittest

from aaa192.test.r3_fixtures import make_product, make_store
from stock_control.models import Category
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store


def status_for(quantity, min_level, max_level):
    store = Store()
    store.categories["Tools"] = Category("Tools")
    store.products["TLS-0001"] = make_product(
        "TLS-0001", quantity, min_level, max_level)
    return stock_level_report(store)[0]["status"]


class TestStockLevelReportConcolic(unittest.TestCase):

    def test_iteration_0_seed_in_stock(self):
        self.assertEqual("in stock", status_for(20, 5, 50))

    def test_iteration_1_negate_s3_overstocked(self):
        self.assertEqual("overstocked", status_for(51, 5, 50))

    def test_iteration_2_negate_s2_low(self):
        self.assertEqual("low", status_for(4, 5, 50))

    def test_iteration_3_negate_s1_out(self):
        self.assertEqual("out", status_for(0, 5, 50))

    def test_iteration_4_negate_d2_unknown_category(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            stock_level_report(make_store(), category="Garden")

    def test_iteration_5_negate_d1_unknown_group(self):
        with self.assertRaisesRegex(ValueError, "cannot group by"):
            stock_level_report(make_store(), group_by="supplier")


if __name__ == "__main__":
    unittest.main()
