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


class TestSearchProductsSymbolicExecution(unittest.TestCase):

    def test_leaf_1_name_not_str(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), 3.5)

    def test_leaf_2_category_not_in_cats(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Z")

    def test_leaf_3_min_lt_zero(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-1)

    def test_leaf_4_max_lt_zero(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-1)

    def test_leaf_5_min_gt_max(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=2, max_price=1)

    def test_leaf_6_availability_not_in_set(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), availability="?")

    def test_leaf_7_found_empty(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "qq")

    def test_leaf_8_found_not_empty(self):
        self.assertEqual(4, len(search_products(make_store())))

    def test_loop_pc_archived(self):
        self.assertNotIn("Old pipe valve",
                         names(search_products(make_store())))

    def test_loop_pc_needle_absent(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(), "tap")))

    def test_loop_pc_category_differs(self):
        self.assertEqual(["Cordless drill", "Pipe cutter"],
                         names(search_products(make_store(),
                                               category="Tools")))

    def test_loop_pc_price_below_min(self):
        self.assertEqual(["Cordless drill", "Pipe cutter"],
                         names(search_products(make_store(), min_price=15)))

    def test_loop_pc_price_above_max(self):
        self.assertEqual(["Brass tap", "Copper pipe"],
                         names(search_products(make_store(), max_price=12)))

    def test_loop_pc_availability_differs(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(),
                                               availability="low")))


if __name__ == "__main__":
    unittest.main()
