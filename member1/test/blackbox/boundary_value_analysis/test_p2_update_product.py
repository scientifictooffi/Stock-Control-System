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


class TestUpdateProductBoundaryValues(unittest.TestCase):

    def test_price_just_above_zero(self):
        product = update_product(make_store(), "TAP-0001", {"price": 0.01})
        self.assertEqual(0.01, product.price)

    def test_price_exactly_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": 0})

    def test_price_just_below_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": -0.01})

    def test_cost_zero(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 0})
        self.assertEqual(0, product.cost)

    def test_cost_just_above_zero(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 0.01})
        self.assertEqual(0.01, product.cost)

    def test_cost_just_below_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -0.01})

    def test_name_length_one(self):
        product = update_product(make_store(), "TAP-0001", {"name": "T"})
        self.assertEqual("T", product.name)

    def test_name_length_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": ""})

    def test_new_sku_length_eight(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"sku": "TAP-0009"})
        self.assertEqual("TAP-0009", product.sku)

    def test_new_sku_length_seven(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "TAP-009"})

    def test_new_sku_length_nine(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "TAP-00099"})

    def test_one_change(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 1.0})
        self.assertEqual(1.0, product.cost)

    def test_zero_changes(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_all_five_fields(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"sku": "TAP-0002", "name": "Tap",
                                  "category": "Tools", "price": 1.0,
                                  "cost": 0.5})
        self.assertEqual("TAP-0002", product.sku)


if __name__ == "__main__":
    unittest.main()
