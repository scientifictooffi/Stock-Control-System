import unittest

from stock_control.models import Category, Product
from stock_control.products.search import search_products
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.categories["Tools"] = Category("Tools")
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 8.5, 4.0, 40,
                                         min_level=5)
    store.products["TAP-0001"] = Product("TAP-0001", "Brass tap",
                                         "Plumbing", 12.0, 6.0, 3,
                                         min_level=5)
    store.products["DRL-0001"] = Product("DRL-0001", "Cordless drill",
                                         "Tools", 89.0, 55.0, 0,
                                         min_level=1)
    store.products["CUT-0001"] = Product("CUT-0001", "Pipe cutter",
                                         "Tools", 15.0, 7.0, 10,
                                         min_level=5)
    store.products["OLD-0001"] = Product("OLD-0001", "Old pipe valve",
                                         "Plumbing", 3.0, 1.0, 9,
                                         status="archived")
    return store


def names(products):
    return [product.name for product in products]


class TestSearchProductsStatementCoverage(unittest.TestCase):

    def test_raise_name_type(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), None)

    def test_raise_category(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Zoo")

    def test_raise_min_negative(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-1)

    def test_raise_max_negative(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-1)

    def test_raise_min_above_max(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=2, max_price=1)

    def test_raise_availability(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="x")

    def test_raise_nothing_found(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "nothing")

    def test_every_continue_and_return(self):
        result = search_products(make_store(), "pipe", "Tools", 1, 50,
                                 "in_stock")
        self.assertEqual(["Pipe cutter"], names(result))


if __name__ == "__main__":
    unittest.main()
