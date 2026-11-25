import unittest
from ab1409.test.s2_fixtures import (
    ACME, ARCHIVED_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, make_store_with_preferred, snapshot)
from stock_control.purchasing.suppliers import link_product_supplier


class TestLinkProductSupplierPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store_with_preferred()
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args, **kwargs):
        with self.assertRaises(error) as ctx:
            link_product_supplier(self.store, *args, **kwargs)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def test_path_1_unknown_product(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, ACME, 5.0, 7)

    def test_path_2_product_not_active(self):
        self.assert_path_refused(
            ValueError, "not active", ARCHIVED_SKU, ACME, 5.0, 7)

    def test_path_3_unknown_supplier(self):
        self.assert_path_refused(
            KeyError, "does not exist", TAP_SKU, UNKNOWN_ID, 5.0, 7)

    def test_path_4_supplier_not_active(self):
        self.assert_path_refused(
            ValueError, "not active", TAP_SKU, SUSPENDED_ID, 5.0, 7)

    def test_path_5_bad_price(self):
        self.assert_path_refused(
            ValueError, "price", TAP_SKU, ACME, 0.0, 7)

    def test_path_5_bad_price_bool(self):
        self.assert_path_refused(
            ValueError, "price", TAP_SKU, ACME, True, 7)

    def test_path_6_bad_delivery_time(self):
        self.assert_path_refused(
            ValueError, "1 to 90", TAP_SKU, ACME, 5.0, 0)

    def test_path_7_bad_pack_size(self):
        self.assert_path_refused(
            ValueError, "pack size", TAP_SKU, ACME, 5.0, 7, pack_size=-4)

    def test_path_8_preferred_not_bool(self):
        self.assert_path_refused(
            ValueError, "True or False", TAP_SKU, ACME, 5.0, 7,
            preferred="yes")

    def test_path_9_second_preferred_supplier(self):
        self.assert_path_refused(
            ValueError, "already has a preferred", PIPE_SKU, DELTA, 4.0, 7,
            preferred=True)

    def test_path_10_update_existing_link(self):
        link = link_product_supplier(
            self.store, PIPE_SKU, DELTA, 4.25, 12, False, 5)
        self.assertEqual(len(self.store.product_suppliers), 2)
        self.assertEqual((link.price, link.lead_time_days, link.pack_size),
                         (4.25, 12, 5))
        self.assertEqual(self.store.products[PIPE_SKU].preferred_supplier,
                         ACME)

    def test_path_11_create_new_link(self):
        store = make_store()
        link = link_product_supplier(store, TAP_SKU, ACME, 11.0, 6, True, 4)
        self.assertEqual(store.product_suppliers, [link])
        self.assertEqual(store.products[TAP_SKU].preferred_supplier, ACME)


if __name__ == "__main__":
    unittest.main()
