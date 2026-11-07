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


class TestUpdateProductStatementCoverage(unittest.TestCase):

    def test_raise_not_found(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "NOP-0000", {"name": "x"})

    def test_raise_archived(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"name": "x"})

    def test_raise_no_changes(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_raise_unknown_field(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"weight": 1})

    def test_raise_sku_history(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_raise_sku_format(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "bad"})

    def test_raise_sku_duplicate(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "OLD-0001"})

    def test_raise_name(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": ""})

    def test_raise_category(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Zoo"})

    def test_raise_price(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": -1})

    def test_raise_cost(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -1})

    def test_success_every_field_including_sku_rename(self):
        store = make_store()
        product = update_product(store, "TAP-0001",
                                 {"sku": "TAP-0002", "name": " Tap ",
                                  "category": "Tools", "price": 2.0,
                                  "cost": 1.0})
        self.assertEqual("Tap", product.name)
        self.assertIs(product, store.products["TAP-0002"])


if __name__ == "__main__":
    unittest.main()
