import unittest

from stock_control.models import Category
from stock_control.products.catalogue import add_product
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    return store


class TestAddProductBoundaryValues(unittest.TestCase):

    def test_price_just_above_zero_is_accepted(self):
        product = add_product(make_store(), "TAP-0001", "Tap", "Plumbing",
                              0.01)
        self.assertEqual(0.01, product.price)

    def test_price_exactly_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 0)

    def test_price_just_below_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", -0.01)

    def test_quantity_zero_is_accepted(self):
        product = add_product(make_store(), "TAP-0001", "Tap", "Plumbing",
                              5.0, 0)
        self.assertEqual(0, product.quantity)

    def test_quantity_one_is_accepted(self):
        product = add_product(make_store(), "TAP-0001", "Tap", "Plumbing",
                              5.0, 1)
        self.assertEqual(1, product.quantity)

    def test_quantity_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "Tap", "Plumbing", 5.0, -1)

    def test_sku_length_eight_is_accepted(self):
        product = add_product(make_store(), "ABC-1234", "Tap", "Plumbing",
                              5.0)
        self.assertEqual("ABC-1234", product.sku)

    def test_sku_length_seven_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "ABC-123", "Tap", "Plumbing", 5.0)

    def test_sku_length_nine_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "ABC-12345", "Tap", "Plumbing", 5.0)

    def test_name_length_one_is_accepted(self):
        product = add_product(make_store(), "TAP-0001", "T", "Plumbing", 5.0)
        self.assertEqual("T", product.name)

    def test_name_length_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            add_product(make_store(), "TAP-0001", "", "Plumbing", 5.0)


if __name__ == "__main__":
    unittest.main()
