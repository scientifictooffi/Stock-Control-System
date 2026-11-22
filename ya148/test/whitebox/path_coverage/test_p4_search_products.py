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


class TestSearchProductsPathCoverage(unittest.TestCase):

    def test_path_1_name_type_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), b"pipe")

    def test_path_2_category_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Zoo")

    def test_path_3_min_negative_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-3)

    def test_path_4_max_negative_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-3)

    def test_path_5_min_above_max_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=3, max_price=2)

    def test_path_6_availability_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="some")

    def test_path_7_loop_skips_archived_then_found(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "pipe")))

    def test_path_8_loop_skips_by_name_then_empty(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "nothing")

    def test_path_9_loop_skips_by_category(self):
        self.assertEqual(["Brass tap", "Copper pipe"],
                         names(search_products(make_store(),
                                               category="Plumbing")))

    def test_path_10_loop_skips_by_min_price(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(), min_price=20)))

    def test_path_11_loop_skips_by_max_price(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), max_price=10)))

    def test_path_12_loop_skips_by_availability(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               availability="out")))

    def test_path_13_empty_store(self):
        with self.assertRaises(LookupError):
            search_products(Store())

    def test_path_14_all_filters_all_pass(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(), "cutter",
                                               "Tools", 10, 20, "in_stock")))


if __name__ == "__main__":
    unittest.main()
