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


class TestSearchProductsBranchCoverage(unittest.TestCase):

    def test_name_not_str_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), 1)

    def test_category_given_and_missing_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Zoo")

    def test_min_negative_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-1)

    def test_max_negative_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-1)

    def test_min_above_max_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=9, max_price=1)

    def test_availability_bad_true(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="bad")

    def test_archived_skipped_true(self):
        self.assertNotIn("Old pipe valve",
                         names(search_products(make_store(), "pipe")))

    def test_name_mismatch_true(self):
        self.assertNotIn("Brass tap",
                         names(search_products(make_store(), "pipe")))

    def test_category_mismatch_true(self):
        self.assertNotIn("Brass tap",
                         names(search_products(make_store(),
                                               category="Tools")))

    def test_min_price_mismatch_true(self):
        self.assertNotIn("Copper pipe",
                         names(search_products(make_store(), min_price=10)))

    def test_max_price_mismatch_true(self):
        self.assertNotIn("Cordless drill",
                         names(search_products(make_store(), max_price=20)))

    def test_availability_mismatch_true(self):
        self.assertNotIn("Brass tap",
                         names(search_products(make_store(),
                                               availability="in_stock")))

    def test_nothing_found_true(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "zzz")

    def test_all_false_no_filters(self):
        self.assertEqual(4, len(search_products(make_store())))

    def test_all_false_with_every_filter_matching(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "copper",
                                               "Plumbing", 1, 10,
                                               "in_stock")))

    def test_availability_out_branch(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               availability="out")))

    def test_availability_low_branch(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(),
                                               availability="low")))


if __name__ == "__main__":
    unittest.main()
