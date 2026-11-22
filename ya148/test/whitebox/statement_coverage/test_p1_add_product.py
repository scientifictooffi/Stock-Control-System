import unittest

from stock_control.models import Category, Product
from stock_control.products.catalogue import _is_valid_sku, add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    return store


class TestAddProductStatementCoverage(unittest.TestCase):

    def test_statement_raise_invalid_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "bad", "Tap", "Plumbing", 1.0)

    def test_statement_raise_duplicate_sku(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "PIP-0001", "Tap", "Plumbing", 1.0)

    def test_statement_raise_name_required(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", " ", "Plumbing", 1.0)

    def test_statement_raise_price(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 0)

    def test_statement_raise_quantity(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 1.0, -1)

    def test_statement_raise_category(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Garden", 1.0)

    def test_statements_success_path(self):
        store = make_store()
        product = add_product(store, "TAP-0001", " Tap ", "Plumbing", 1.0, 2,
                              0.5)
        self.assertEqual("Tap", product.name)
        self.assertEqual(0.5, product.cost)
        self.assertIn("TAP-0001", store.products)

    def test_statement_sku_not_a_string(self):
        self.assertFalse(_is_valid_sku(None))


if __name__ == "__main__":
    unittest.main()
