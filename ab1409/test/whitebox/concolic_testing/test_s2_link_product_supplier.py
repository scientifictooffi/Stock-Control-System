import unittest
from stock_control.models import Product, ProductSupplier, Supplier
from stock_control.purchasing.suppliers import link_product_supplier
from stock_control.store import Store


def make_store():
    store = Store()
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    store.products["OLD-0001"] = Product(
        "OLD-0001", "Old tap", "Plumbing", 2.0, status="archived")
    store.suppliers["SUP0001"] = Supplier(
        "SUP0001", "Acme", "a@acme.co", "01164960001")
    store.suppliers["SUP0002"] = Supplier(
        "SUP0002", "Delta", "d@delta.co", "01164960002")
    store.suppliers["SUP0003"] = Supplier(
        "SUP0003", "Sigma", "s@sigma.co", "01164960003", "suspended")
    store.product_suppliers.append(
        ProductSupplier("PIP-0001", "SUP0001", 5.0, 3, 1, True))
    return store


class TestLinkProductSupplierConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_new_link(self):
        store = make_store()
        link = link_product_supplier(
            store, "PIP-0001", "SUP0002", 4.0, 7, False, 1)
        self.assertEqual(2, len(store.product_suppliers))
        self.assertEqual("SUP0002", link.supplier_id)

    def test_iteration_1_negate_d10_link_already_exists(self):
        store = make_store()
        link_product_supplier(store, "PIP-0001", "SUP0001", 4.0, 7, True, 1)
        self.assertEqual(1, len(store.product_suppliers))
        self.assertEqual(4.0, store.product_suppliers[0].price)

    def test_iteration_2_negate_d9_other_supplier_preferred(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                make_store(), "PIP-0001", "SUP0002", 4.0, 7, True, 1)

    def test_iteration_3_negate_d8_preferred_not_bool(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                make_store(), "PIP-0001", "SUP0002", 4.0, 7, "yes", 1)

    def test_iteration_4_negate_d7_pack_size_invalid(self):
        for size in (0, 1.5):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", 4.0, 7, False,
                        size)

    def test_iteration_5_negate_d6_delivery_time_invalid(self):
        for days in (0, 91, 7.5):
            with self.subTest(days=days):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", 4.0, days)

    def test_iteration_6_negate_d5_price_invalid(self):
        for price in (0, -2.5, "4", False):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", price, 7)

    def test_iteration_7_negate_d4_supplier_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(make_store(), "PIP-0001", "SUP0003", 4.0, 7)

    def test_iteration_8_negate_d3_supplier_unknown(self):
        with self.assertRaises(KeyError):
            link_product_supplier(make_store(), "PIP-0001", "SUP0042", 4.0, 7)

    def test_iteration_9_negate_d2_product_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(make_store(), "OLD-0001", "SUP0002", 4.0, 7)

    def test_iteration_10_negate_d1_product_unknown(self):
        with self.assertRaises(KeyError):
            link_product_supplier(make_store(), "TAP-0001", "SUP0002", 4.0, 7)


if __name__ == "__main__":
    unittest.main()
