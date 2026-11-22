import unittest

from stock_control.models import Category, Movement, Product
from stock_control.products.catalogue import update_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.categories["Tools"] = Category("Tools")
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 4.5, 2.0, 10)
    store.products["TAP-0001"] = Product("TAP-0001", "Brass tap",
                                         "Plumbing", 12.0)
    store.products["OLD-0001"] = Product("OLD-0001", "Old valve",
                                         "Plumbing", 3.0, status="archived")
    store.movements.append(Movement("MV-1", "PIP-0001", "receipt", 10,
                                    "Main", "2026-11-03"))
    return store


class TestUpdateProductBranchCoverage(unittest.TestCase):

    def test_product_missing_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "NOP-0000", {"name": "x"})

    def test_archived_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"name": "x"})

    def test_no_changes_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_field_not_editable_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"status": "x"})

    def test_sku_history_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_sku_invalid_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "x"})

    def test_sku_duplicate_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "PIP-0001"})

    def test_sku_all_false(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"sku": "TAP-0002"})
        self.assertEqual("TAP-0002", product.sku)

    def test_name_not_string_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": None})

    def test_name_blank_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": " "})

    def test_name_false(self):
        product = update_product(make_store(), "TAP-0001", {"name": "Tap"})
        self.assertEqual("Tap", product.name)

    def test_category_missing_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Zoo"})

    def test_category_false(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"category": "Tools"})
        self.assertEqual("Tools", product.category)

    def test_price_bad_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": 0})

    def test_price_false(self):
        product = update_product(make_store(), "TAP-0001", {"price": 1})
        self.assertEqual(1, product.price)

    def test_cost_bad_true(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -1})

    def test_cost_false_and_sku_not_in_changes(self):
        store = make_store()
        product = update_product(store, "TAP-0001", {"cost": 1})
        self.assertEqual(1, product.cost)
        self.assertIn("TAP-0001", store.products)


if __name__ == "__main__":
    unittest.main()
