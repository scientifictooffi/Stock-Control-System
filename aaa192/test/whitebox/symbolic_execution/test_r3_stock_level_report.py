"""R3 stock_level_report - white-box: symbolic execution.

One test per leaf of the symbolic execution tree in
docs/research/R3_stock_level_report.md, using the solution of that
leaf's path condition (PC).
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


class TestStockLevelReportSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_group_unknown(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), group_by="supplier")

    def test_leaf_l2_pc_category_unknown(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), category="Garden")

    def test_leaf_l3_pc_quantity_zero(self):
        self.assertEqual("out", status_for(0, 5, 50))

    def test_leaf_l4_pc_quantity_below_min(self):
        self.assertEqual("low", status_for(3, 5, 50))

    def test_leaf_l5_pc_quantity_above_max(self):
        self.assertEqual("overstocked", status_for(60, 5, 50))

    def test_leaf_l6_pc_between_levels(self):
        self.assertEqual("in stock", status_for(20, 5, 50))

    def test_leaf_l7_pc_no_max_set(self):
        self.assertEqual("in stock", status_for(60, 5, 0))


if __name__ == "__main__":
    unittest.main()
