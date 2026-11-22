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


class TestSearchProductsEquivalencePartitioning(unittest.TestCase):

    def test_empty_name_returns_all_active_products(self):
        self.assertEqual(["Brass tap", "Copper pipe", "Cordless drill",
                          "Pipe cutter"], names(search_products(make_store())))

    def test_partial_name_matches(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "pipe")))

    def test_name_is_case_insensitive(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(), "BRASS")))

    def test_name_not_found_raises(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "hammer")

    def test_name_not_string_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), 42)

    def test_category_filter(self):
        self.assertEqual(["Cordless drill", "Pipe cutter"],
                         names(search_products(make_store(),
                                               category="Tools")))

    def test_unknown_category_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Garden")

    def test_price_range_filter(self):
        self.assertEqual(["Brass tap", "Pipe cutter"],
                         names(search_products(make_store(), min_price=10,
                                               max_price=20)))

    def test_min_above_max_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=20, max_price=10)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-1)

    def test_availability_in_stock(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(),
                                               availability="in_stock")))

    def test_availability_low(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(),
                                               availability="low")))

    def test_availability_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               availability="out")))

    def test_unknown_availability_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="plenty")

    def test_archived_products_never_returned(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "valve")

    def test_all_filters_together(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(), "pipe", "Tools",
                                               10, 20, "in_stock")))


if __name__ == "__main__":
    unittest.main()
