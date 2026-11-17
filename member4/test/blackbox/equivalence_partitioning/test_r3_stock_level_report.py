"""R3 stock_level_report - black-box: equivalence partitioning.

Input classes taken from the four rules:
group_by: "product" | "warehouse" (valid) | anything else (invalid)
category: None | existing category (valid) | unknown category (invalid)
status of a line: out | low | in stock | overstocked
store: has products | empty
One test per class.
"""
import unittest

from member4.test.r3_fixtures import make_store, statuses
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store


class TestStockLevelReportEquivalencePartitioning(unittest.TestCase):

    def test_group_by_product(self):
        lines = stock_level_report(make_store())
        self.assertEqual(5, len(lines))

    def test_group_by_warehouse(self):
        lines = stock_level_report(make_store(), group_by="warehouse")
        self.assertEqual(5, len(lines))
        self.assertIn("warehouse", lines[0])

    def test_invalid_group_by(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), group_by="supplier")

    def test_existing_category(self):
        lines = stock_level_report(make_store(), category="Paint")
        self.assertEqual(["PNT-0001", "PNT-0002"],
                         [line["sku"] for line in lines])

    def test_unknown_category(self):
        with self.assertRaises(ValueError):
            stock_level_report(make_store(), category="Garden")

    def test_each_status_class(self):
        result = statuses(stock_level_report(make_store()))
        self.assertEqual("out", result["TLS-0001"])
        self.assertEqual("low", result["TLS-0002"])
        self.assertEqual("in stock", result["TLS-0003"])
        self.assertEqual("overstocked", result["PNT-0001"])

    def test_empty_store(self):
        self.assertEqual([], stock_level_report(Store()))


if __name__ == "__main__":
    unittest.main()
