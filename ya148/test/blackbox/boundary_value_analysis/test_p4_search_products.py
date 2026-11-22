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


class TestSearchProductsBoundaryValues(unittest.TestCase):

    def test_min_price_equal_to_product_price_included(self):
        self.assertIn("Brass tap", names(search_products(make_store(),
                                                         min_price=12.0)))

    def test_min_price_just_above_product_price_excluded(self):
        self.assertNotIn("Brass tap", names(search_products(make_store(),
                                                            min_price=12.01)))

    def test_max_price_equal_to_product_price_included(self):
        self.assertIn("Brass tap", names(search_products(make_store(),
                                                         max_price=12.0)))

    def test_max_price_just_below_product_price_excluded(self):
        self.assertNotIn("Brass tap", names(search_products(make_store(),
                                                            max_price=11.99)))

    def test_min_price_zero_accepted(self):
        self.assertEqual(4, len(search_products(make_store(), min_price=0)))

    def test_min_price_just_below_zero_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=-0.01)

    def test_min_equal_max_accepted(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(), min_price=12,
                                               max_price=12)))

    def test_min_just_above_max_rejected(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=12.01, max_price=12)

    def test_quantity_zero_is_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               availability="out")))

    def test_quantity_one_below_min_level_is_low(self):
        store = make_store()
        store.products["TAP-0001"].quantity = 4
        self.assertIn("Brass tap",
                      names(search_products(store, availability="low")))

    def test_quantity_equal_to_min_level_is_in_stock(self):
        store = make_store()
        store.products["TAP-0001"].quantity = 5
        self.assertIn("Brass tap",
                      names(search_products(store, availability="in_stock")))

    def test_quantity_one_with_min_level_one_is_in_stock(self):
        store = make_store()
        store.products["DRL-0001"].quantity = 1
        self.assertIn("Cordless drill",
                      names(search_products(store, availability="in_stock")))

    def test_one_character_name(self):
        self.assertEqual(["Brass tap", "Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "p")))

    def test_name_longer_than_any_product_name(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "x" * 100)


if __name__ == "__main__":
    unittest.main()
