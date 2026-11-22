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


class TestUpdateProductPathCoverage(unittest.TestCase):

    def test_path_1_not_found(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "NOP-0000", {"name": "x"})

    def test_path_2_archived(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "OLD-0001", {"name": "x"})

    def test_path_3_empty_changes(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {})

    def test_path_4_unknown_field(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"size": 1})

    def test_path_5_sku_with_history(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "PIP-0001", {"sku": "PIP-0002"})

    def test_path_6_sku_bad_format(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "nope"})

    def test_path_7_sku_duplicate(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"sku": "OLD-0001"})

    def test_path_8_sku_ok_rename(self):
        store = make_store()
        update_product(store, "TAP-0001", {"sku": "TAP-0002"})
        self.assertNotIn("TAP-0001", store.products)

    def test_path_9_name_blank(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"name": ""})

    def test_path_10_name_ok(self):
        product = update_product(make_store(), "TAP-0001", {"name": "Tap"})
        self.assertEqual("Tap", product.name)

    def test_path_11_category_missing(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"category": "Zoo"})

    def test_path_12_category_ok(self):
        product = update_product(make_store(), "TAP-0001",
                                 {"category": "Tools"})
        self.assertEqual("Tools", product.category)

    def test_path_13_price_bad(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"price": 0})

    def test_path_14_price_ok(self):
        product = update_product(make_store(), "TAP-0001", {"price": 5})
        self.assertEqual(5, product.price)

    def test_path_15_cost_bad(self):
        with self.assertRaises(ValueError):
            update_product(make_store(), "TAP-0001", {"cost": -2})

    def test_path_16_cost_ok(self):
        product = update_product(make_store(), "TAP-0001", {"cost": 2})
        self.assertEqual(2, product.cost)

    def test_path_17_loop_twice_second_fails(self):
        store = make_store()
        with self.assertRaises(ValueError):
            update_product(store, "TAP-0001", {"name": "Tap", "price": 0})
        self.assertEqual("Brass tap", store.products["TAP-0001"].name)


if __name__ == "__main__":
    unittest.main()
