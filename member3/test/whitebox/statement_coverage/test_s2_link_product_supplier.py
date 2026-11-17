import unittest
from member3.test.s2_fixtures import (
    ACME, ARCHIVED_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, make_store_with_preferred)
from stock_control.purchasing.suppliers import link_product_supplier


class TestLinkProductSupplierStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_statement_raise_unknown_product(self):
        with self.assertRaises(KeyError):
            link_product_supplier(self.store, UNKNOWN_SKU, ACME, 5.0, 7)

    def test_statement_raise_product_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, ARCHIVED_SKU, ACME, 5.0, 7)

    def test_statement_raise_unknown_supplier(self):
        with self.assertRaises(KeyError):
            link_product_supplier(self.store, PIPE_SKU, UNKNOWN_ID, 5.0, 7)

    def test_statement_raise_supplier_not_active(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, SUSPENDED_ID, 5.0, 7)

    def test_statement_raise_price(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, 0, 7)

    def test_statement_raise_delivery_time(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, 5.0, 91)

    def test_statement_raise_pack_size(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                self.store, PIPE_SKU, ACME, 5.0, 7, pack_size=0)

    def test_statement_raise_preferred_not_bool(self):
        with self.assertRaises(ValueError):
            link_product_supplier(
                self.store, PIPE_SKU, ACME, 5.0, 7, preferred=1)

    def test_statement_raise_second_preferred(self):
        store = make_store_with_preferred()
        with self.assertRaises(ValueError):
            link_product_supplier(
                store, PIPE_SKU, DELTA, 4.0, 7, preferred=True)

    def test_statements_create_link_and_set_preferred(self):
        link = link_product_supplier(
            self.store, TAP_SKU, ACME, 12.5, 4, True, 6)
        self.assertEqual(self.store.product_suppliers, [link])
        self.assertEqual(self.store.products[TAP_SKU].preferred_supplier,
                         ACME)

    def test_statements_update_link_and_clear_preferred(self):
        store = make_store_with_preferred()
        link = link_product_supplier(
            store, PIPE_SKU, ACME, 6.0, 9, False, 12)
        self.assertEqual((link.price, link.lead_time_days, link.pack_size,
                          link.preferred), (6.0, 9, 12, False))
        self.assertEqual(len(store.product_suppliers), 2)
        self.assertIsNone(store.products[PIPE_SKU].preferred_supplier)

    def test_statement_price_not_a_number(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, "5", 7)


if __name__ == "__main__":
    unittest.main()
