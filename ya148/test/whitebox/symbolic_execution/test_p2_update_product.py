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


class TestUpdateProductSymbolicExecution(unittest.TestCase):

    def test_leaf_1_sku_not_in_products(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "NOP-0000", {"name": "x"})

    def test_leaf_2_status_archived(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"name": "x"})

    def test_leaf_3_changes_empty(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_leaf_4_field_not_editable(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"box_size": 2})

    def test_leaf_5_sku_and_history(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_leaf_6_sku_and_not_valid(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "TAP-1"})

    def test_leaf_7_sku_and_in_products(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "PIP-0001"})

    def test_leaf_8_sku_valid_new(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"sku": "TAP-0003"})
        self.assertEqual("TAP-0003", product.sku)

    def test_leaf_9_name_blank(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": "\t"})

    def test_leaf_10_name_ok(self):
        product = update_product(make_store(), "TAP-0001", {"name": "N"})
        self.assertEqual("N", product.name)

    def test_leaf_11_category_unknown(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Z"})

    def test_leaf_12_category_ok(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"category": "Tools"})
        self.assertEqual("Tools", product.category)

    def test_leaf_13_price_le_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": -3})

    def test_leaf_14_price_gt_zero(self):
        product = update_product(make_store(), "TAP-0001", {"price": 3})
        self.assertEqual(3, product.price)

    def test_leaf_15_cost_lt_zero(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -3})

    def test_leaf_16_cost_ge_zero(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 0})
        self.assertEqual(0, product.cost)


if __name__ == "__main__":
    unittest.main()
