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


class TestSearchProductsConcolic(unittest.TestCase):

    def test_iteration_0_seed_no_filters(self):
        self.assertEqual(4, len(search_products(make_store())))

    def test_iteration_1_negate_found_not_empty(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "zzz")

    def test_iteration_2_negate_availability_valid(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="zzz")

    def test_iteration_3_negate_min_le_max(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=5, max_price=4)

    def test_iteration_4_negate_max_ge_zero(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-4)

    def test_iteration_5_negate_min_ge_zero(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-4)

    def test_iteration_6_negate_category_exists(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="zzz")

    def test_iteration_7_negate_name_is_str(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), ["pipe"])

    def test_iteration_8_loop_negate_needle_match(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "pipe")))

    def test_iteration_9_loop_negate_category_match(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "pipe",
                                               "Plumbing")))

    def test_iteration_10_loop_negate_min_price_match(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(), "pipe",
                                               min_price=10)))

    def test_iteration_11_loop_negate_max_price_match(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "pipe",
                                               max_price=10)))

    def test_iteration_12_loop_negate_availability_match(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "pipe", availability="out")

    def test_iteration_13_loop_negate_not_archived(self):
        store = make_store()
        store.products["OLD-0001"].status = "active"
        self.assertIn("Old pipe valve",
                      names(search_products(store, "valve")))


if __name__ == "__main__":
    unittest.main()
