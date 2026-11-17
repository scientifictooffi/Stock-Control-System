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


class TestLinkProductSupplierSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_sku_unknown(self):
        with self.assertRaises(KeyError):
            link_product_supplier(make_store(), "TAP-0001", "SUP0001", 5, 7)

    def test_leaf_l2_pc_product_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(make_store(), "OLD-0001", "SUP0001", 5, 7)

    def test_leaf_l3_pc_supplier_unknown(self):
        with self.assertRaises(KeyError):
            link_product_supplier(make_store(), "PIP-0001", "SUP0009", 5, 7)

    def test_leaf_l4_pc_supplier_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(make_store(), "PIP-0001", "SUP0003", 5, 7)

    def test_leaf_l5_pc_price_invalid(self):
        for price in (0, -1, "5", True, float("inf")):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", price, 7)

    def test_leaf_l6_pc_lead_time_invalid(self):
        for days in (0, 91, 2.5, "7"):
            with self.subTest(days=days):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", 5, days)

    def test_leaf_l7_pc_pack_size_invalid(self):
        for size in (0, 2.5, "3"):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    link_product_supplier(
                        make_store(), "PIP-0001", "SUP0002", 5, 7,
                        pack_size=size)

    def test_leaf_l8_pc_preferred_not_bool(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                make_store(), "PIP-0001", "SUP0002", 5, 7, preferred=1)

    def test_leaf_l9_pc_other_supplier_is_preferred(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                make_store(), "PIP-0001", "SUP0002", 5, 7, preferred=True)

    def test_leaf_l10_pc_link_exists(self):
        store = make_store()
        link = link_product_supplier(
            store, "PIP-0001", "SUP0001", 6, 8, preferred=True)
        self.assertEqual(1, len(store.product_suppliers))
        self.assertEqual((6, 8), (link.price, link.lead_time_days))

    def test_leaf_l11_pc_link_new(self):
        store = make_store()
        link_product_supplier(store, "PIP-0001", "SUP0002", 6, 8)
        self.assertEqual(2, len(store.product_suppliers))
        self.assertEqual(
            "SUP0001", store.products["PIP-0001"].preferred_supplier)


if __name__ == "__main__":
    unittest.main()
