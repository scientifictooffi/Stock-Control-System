import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import _is_valid_sku, add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    return store


class TestAddProductBranchCoverage(unittest.TestCase):

    def test_branch_sku_invalid_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-", "Tap", "Plumbing", 1.0)

    def test_branch_sku_duplicate_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Tap", "Plumbing", 1.0)

    def test_branch_name_not_string_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", None, "Plumbing", 1.0)

    def test_branch_name_blank_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "", "Plumbing", 1.0)

    def test_branch_price_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", -1.0)

    def test_branch_quantity_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 1.0, -5)

    def test_branch_category_true(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Tools", 1.0)

    def test_all_branches_false_success(self):
        store = make_store()
        product = add_product(store, "TAP-0001", "Tap", "Plumbing", 1.0, 3)
        self.assertEqual(3, store.products["TAP-0001"].quantity)
        self.assertIs(product, store.products["TAP-0001"])

    def test_is_valid_sku_both_branches(self):
        self.assertFalse(_is_valid_sku(123))
        self.assertTrue(_is_valid_sku("ABC-0001"))
        self.assertFalse(_is_valid_sku("ABC-001"))


if __name__ == "__main__":
    unittest.main()
