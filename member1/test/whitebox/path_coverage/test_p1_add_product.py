import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    return store


class TestAddProductPathCoverage(unittest.TestCase):

    def test_path_1_invalid_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "xx", "Tap", "Plumbing", 1.0, 1)

    def test_path_2_duplicate_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Tap", "Plumbing", 1.0, 1)

    def test_path_3_blank_name(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "", "Plumbing", 1.0, 1)

    def test_path_4_bad_price(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 0, 1)

    def test_path_5_bad_quantity(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 1.0, -1)

    def test_path_6_unknown_category(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Garden", 1.0, 1)

    def test_path_7_success(self):
        store = make_store()
        product = add_product(store, "TAP-0001", "Tap", "Plumbing", 1.0, 1)
        self.assertEqual("Plumbing", product.category)
        self.assertEqual(2, len(store.products))


if __name__ == "__main__":
    unittest.main()
