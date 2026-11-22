"""R3 stock_level_report - black-box: boundary value analysis.

The boundaries are the edges of each status: quantity 0 and 1, just
below / at the minimum, at / just above the maximum, and a maximum of 0
(no maximum set). Levels used: min_level 5, max_level 50.
"""
import unittest

from aaa192.test.r3_fixtures import make_product
from stock_control.models import Category
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store


def status_for(quantity, min_level=5, max_level=50):
    store = Store()
    store.categories["Tools"] = Category("Tools")
    store.products["TLS-0001"] = make_product(
        "TLS-0001", quantity, min_level, max_level)
    return stock_level_report(store)[0]["status"]


class TestStockLevelReportBoundaryValues(unittest.TestCase):

    def test_quantity_zero_is_out(self):
        self.assertEqual("out", status_for(0))

    def test_quantity_one_is_low(self):
        self.assertEqual("low", status_for(1))

    def test_just_below_minimum_is_low(self):
        self.assertEqual("low", status_for(4))

    def test_at_minimum_is_in_stock(self):
        self.assertEqual("in stock", status_for(5))

    def test_at_maximum_is_in_stock(self):
        self.assertEqual("in stock", status_for(50))

    def test_just_above_maximum_is_overstocked(self):
        self.assertEqual("overstocked", status_for(51))

    def test_no_maximum_never_overstocked(self):
        self.assertEqual("in stock", status_for(10000, max_level=0))

    def test_minimum_zero_quantity_one_in_stock(self):
        self.assertEqual("in stock", status_for(1, min_level=0))


if __name__ == "__main__":
    unittest.main()
