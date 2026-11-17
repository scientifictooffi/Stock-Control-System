"""R3 stock_level_report - black-box: random testing.

200 random products (quantity, min_level, max_level, category, status)
with a fixed seed so the run can be repeated. Each line is checked
against an oracle written from the rules.
"""
import random
import unittest

from member4.test.r3_fixtures import make_product
from stock_control.models import Category
from stock_control.reporting.reports import stock_level_report
from stock_control.store import Store

SEED = 42
RUNS = 200


def oracle(quantity, min_level, max_level):
    if quantity == 0:
        return "out"
    if quantity < min_level:
        return "low"
    if max_level and quantity > max_level:
        return "overstocked"
    return "in stock"


class TestStockLevelReportRandom(unittest.TestCase):

    def test_random_products_follow_the_rules(self):
        rng = random.Random(SEED)
        store = Store()
        store.categories["Tools"] = Category("Tools")
        expected = {}
        for number in range(RUNS):
            sku = f"TLS-{number:04d}"
            quantity = rng.randint(0, 120)
            min_level = rng.randint(0, 30)
            max_level = rng.choice([0, rng.randint(min_level + 1, 100)])
            status = rng.choice(["active", "active", "archived"])
            store.products[sku] = make_product(
                sku, quantity, min_level, max_level, status=status)
            if status == "active":
                expected[sku] = oracle(quantity, min_level, max_level)
        lines = stock_level_report(store)
        self.assertEqual(sorted(expected), [line["sku"] for line in lines])
        for line in lines:
            self.assertEqual(expected[line["sku"]], line["status"])


if __name__ == "__main__":
    unittest.main()
