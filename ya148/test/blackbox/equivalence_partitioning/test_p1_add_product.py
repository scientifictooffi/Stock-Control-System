import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 4.5)
    return store


class TestAddProductEquivalencePartitioning(unittest.TestCase):

    def test_valid_class_all_rules_pass(self):
        store = make_store()
        product = add_product(store, "TAP-0001", "Brass tap", "Plumbing",
                              12.0, 5)
        self.assertEqual("TAP-0001", product.sku)
        self.assertIs(product, store.products["TAP-0001"])

    def test_invalid_sku_lowercase(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "tap-0001", "Brass tap", "Plumbing",
                        12.0)

    def test_invalid_sku_no_dash(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP0001", "Brass tap", "Plumbing",
                        12.0)

    def test_invalid_sku_not_string(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), 1001, "Brass tap", "Plumbing", 12.0)

    def test_duplicate_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Copper pipe", "Plumbing",
                        4.5)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "", "Plumbing", 12.0)

    def test_blank_name(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "   ", "Plumbing", 12.0)

    def test_price_zero(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Brass tap", "Plumbing",
                        0)

    def test_price_negative(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Brass tap", "Plumbing",
                        -3.0)

    def test_quantity_negative(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Brass tap", "Plumbing",
                        12.0, -1)

    def test_unknown_category(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Brass tap", "Garden",
                        12.0)


if __name__ == "__main__":
    unittest.main()
