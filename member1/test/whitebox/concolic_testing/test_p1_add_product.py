import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    return store


class TestAddProductConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        store = make_store()
        product = add_product(store, "TAP-0001", "Tap", "Plumbing", 2.0, 1)
        self.assertEqual("TAP-0001", product.sku)

    def test_iteration_1_negate_d6_category(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Garden", 2.0, 1)

    def test_iteration_2_negate_d5_quantity(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 2.0, -1)

    def test_iteration_3_negate_d4_price(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 0.0, 1)

    def test_iteration_4_negate_d3_name(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "  ", "Plumbing", 2.0, 1)

    def test_iteration_5_negate_d2_duplicate(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Tap", "Plumbing", 2.0, 1)

    def test_iteration_6_negate_d1_format(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP0001", "Tap", "Plumbing", 2.0, 1)


if __name__ == "__main__":
    unittest.main()
