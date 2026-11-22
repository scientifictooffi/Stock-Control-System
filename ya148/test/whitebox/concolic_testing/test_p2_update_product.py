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


class TestUpdateProductConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        product = update_product(make_store(), "TAP-0001", {"price": 9.0})
        self.assertEqual(9.0, product.price)

    def test_iteration_1_negate_price_check(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": 0.0})

    def test_iteration_2_negate_field_is_price(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 1.0})
        self.assertEqual(1.0, product.cost)

    def test_iteration_3_negate_cost_check(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -1.0})

    def test_iteration_4_field_is_category_ok(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"category": "Tools"})
        self.assertEqual("Tools", product.category)

    def test_iteration_5_negate_category_check(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Zoo"})

    def test_iteration_6_field_is_name_ok(self):
        product = update_product(make_store(), "TAP-0001", {"name": "Tap"})
        self.assertEqual("Tap", product.name)

    def test_iteration_7_negate_name_check(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": ""})

    def test_iteration_8_field_is_sku_ok(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"sku": "TAP-0002"})
        self.assertEqual("TAP-0002", product.sku)

    def test_iteration_9_negate_sku_duplicate(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "PIP-0001"})

    def test_iteration_10_negate_sku_valid(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "TAP0002"})

    def test_iteration_11_negate_sku_history(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_iteration_12_negate_field_editable(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"owner": "x"})

    def test_iteration_13_negate_changes_not_empty(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_iteration_14_negate_not_archived(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"price": 9.0})

    def test_iteration_15_negate_product_exists(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "NOP-0000", {"price": 9.0})


if __name__ == "__main__":
    unittest.main()
