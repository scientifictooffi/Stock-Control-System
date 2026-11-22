import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    return store


class TestAddProductSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_not_valid_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "tap", "Tap", "Plumbing", 2.0, 1)

    def test_leaf_l2_pc_sku_exists(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Tap", "Plumbing", 2.0, 1)

    def test_leaf_l3_pc_blank_name(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "", "Plumbing", 2.0, 1)

    def test_leaf_l4_pc_price_not_positive(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 0, 1)

    def test_leaf_l5_pc_negative_quantity(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 2.0, -1)

    def test_leaf_l6_pc_unknown_category(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Garden", 2.0, 1)

    def test_leaf_l7_pc_all_rules_hold(self):
        store = make_store()
        product = add_product(store, "TAP-0001", "Tap", "Plumbing", 2.0, 1)
        self.assertIs(product, store.products["TAP-0001"])


if __name__ == "__main__":
    unittest.main()
