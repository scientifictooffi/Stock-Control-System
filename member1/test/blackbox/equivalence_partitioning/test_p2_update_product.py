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


class TestUpdateProductEquivalencePartitioning(unittest.TestCase):

    def test_valid_name_change(self):
        store = make_store()
        product = update_product(store, "TAP-0001", {"name": "Chrome tap"})
        self.assertEqual("Chrome tap", product.name)

    def test_valid_price_change(self):
        product = update_product(make_store(), "TAP-0001", {"price": 15.5})
        self.assertEqual(15.5, product.price)

    def test_valid_several_fields_at_once(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"name": "Tap", "price": 9.0, "cost": 4.0,
                                  "category": "Tools"})
        self.assertEqual(("Tap", 9.0, 4.0, "Tools"),
                         (product.name, product.price, product.cost,
                          product.category))

    def test_valid_sku_change_without_history(self):
        store = make_store()
        product = update_product(store, "TAP-0001", {"sku": "TAP-0002"})
        self.assertEqual("TAP-0002", product.sku)
        self.assertIn("TAP-0002", store.products)
        self.assertNotIn("TAP-0001", store.products)

    def test_unknown_product(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "ZZZ-9999", {"name": "x"})

    def test_archived_product(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"name": "x"})

    def test_empty_changes(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_unknown_field(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"colour": "red"})

    def test_sku_change_with_stock_history(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_sku_change_to_invalid_format(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "tap-2"})

    def test_sku_change_to_existing_sku(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "PIP-0001"})

    def test_blank_name(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": "   "})

    def test_name_not_string(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": 5})

    def test_missing_category(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Garden"})

    def test_price_not_positive(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": 0})

    def test_negative_cost(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -1.0})

    def test_failed_change_leaves_product_untouched(self):
        store = make_store()
        with self.assertRaises(ValueError):
            update_product(store, "TAP-0001", {"name": "New", "price": 0})
        self.assertEqual("Brass tap", store.products["TAP-0001"].name)


if __name__ == "__main__":
    unittest.main()
