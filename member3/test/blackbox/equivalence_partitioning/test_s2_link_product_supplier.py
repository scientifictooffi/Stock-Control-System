import unittest
from member3.test.s2_fixtures import (
    ACME, ARCHIVED_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, make_store_with_preferred, snapshot)
from stock_control.purchasing.suppliers import link_product_supplier


class TestLinkProductSupplierValidClasses(unittest.TestCase):

    def test_valid_class_new_link(self):
        store = make_store()
        link = link_product_supplier(store, PIPE_SKU, ACME, 5.25, 7)
        self.assertEqual(
            (link.sku, link.supplier_id, link.price, link.lead_time_days,
             link.pack_size, link.preferred),
            (PIPE_SKU, ACME, 5.25, 7, 1, False))
        self.assertEqual(store.product_suppliers, [link])

    def test_valid_class_whole_pound_price(self):
        link = link_product_supplier(make_store(), PIPE_SKU, ACME, 5, 7)
        self.assertEqual(link.price, 5)

    def test_valid_class_pack_size(self):
        link = link_product_supplier(
            make_store(), PIPE_SKU, ACME, 5.25, 7, pack_size=10)
        self.assertEqual(link.pack_size, 10)

    def test_valid_class_first_preferred_supplier(self):
        store = make_store()
        link = link_product_supplier(
            store, PIPE_SKU, ACME, 5.25, 7, preferred=True)
        self.assertTrue(link.preferred)
        self.assertEqual(store.products[PIPE_SKU].preferred_supplier, ACME)

    def test_valid_class_two_suppliers_for_one_product(self):
        store = make_store()
        link_product_supplier(store, PIPE_SKU, ACME, 5.25, 7)
        link_product_supplier(store, PIPE_SKU, DELTA, 4.99, 14)
        self.assertEqual(len(store.product_suppliers), 2)

    def test_valid_class_one_supplier_for_two_products(self):
        store = make_store()
        link_product_supplier(store, PIPE_SKU, ACME, 5.25, 7, preferred=True)
        link_product_supplier(store, TAP_SKU, ACME, 12.0, 7, preferred=True)
        self.assertEqual(store.products[TAP_SKU].preferred_supplier, ACME)

    def test_valid_class_not_preferred_while_another_is_preferred(self):
        store = make_store_with_preferred()
        link = link_product_supplier(store, PIPE_SKU, DELTA, 4.50, 10)
        self.assertFalse(link.preferred)
        self.assertEqual(store.products[PIPE_SKU].preferred_supplier, ACME)

    def test_valid_class_existing_link_is_updated(self):
        store = make_store_with_preferred()
        link = link_product_supplier(
            store, PIPE_SKU, DELTA, 4.00, 5, pack_size=20)
        self.assertEqual(len(store.product_suppliers), 2)
        self.assertEqual((link.price, link.lead_time_days, link.pack_size),
                         (4.00, 5, 20))

    def test_valid_class_preferred_supplier_saved_again(self):
        store = make_store_with_preferred()
        link_product_supplier(
            store, PIPE_SKU, ACME, 5.50, 3, preferred=True)
        self.assertEqual(store.products[PIPE_SKU].preferred_supplier, ACME)

    def test_valid_class_change_of_preferred_supplier(self):
        store = make_store_with_preferred()
        link_product_supplier(store, PIPE_SKU, ACME, 5.00, 3, preferred=False)
        self.assertIsNone(store.products[PIPE_SKU].preferred_supplier)
        link_product_supplier(store, PIPE_SKU, DELTA, 4.80, 10, preferred=True)
        self.assertEqual(store.products[PIPE_SKU].preferred_supplier, DELTA)
        self.assertEqual(
            [x.supplier_id for x in store.product_suppliers if x.preferred],
            [DELTA])


class TestLinkProductSupplierInvalidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store_with_preferred()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args, **kwargs):
        with self.assertRaises(error):
            link_product_supplier(self.store, *args, **kwargs)
        self.assertEqual(self.store, self.before)

    def test_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, ACME, 5.0, 7)

    def test_archived_product(self):
        self.assert_refused(ValueError, ARCHIVED_SKU, ACME, 5.0, 7)

    def test_unknown_supplier(self):
        self.assert_refused(KeyError, TAP_SKU, UNKNOWN_ID, 5.0, 7)

    def test_suspended_supplier(self):
        self.assert_refused(ValueError, TAP_SKU, SUSPENDED_ID, 5.0, 7)

    def test_price_zero(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 0, 7)

    def test_price_negative(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, -3.5, 7)

    def test_price_not_a_number(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, "5.00", 7)

    def test_price_is_bool(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, True, 7)

    def test_price_not_finite(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, float("inf"), 7)
        self.assert_refused(ValueError, TAP_SKU, ACME, float("nan"), 7)

    def test_delivery_time_too_short(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 0)

    def test_delivery_time_too_long(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 120)

    def test_delivery_time_not_whole_number(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 7.5)

    def test_delivery_time_is_text(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, "7")

    def test_pack_size_zero(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 7, pack_size=0)

    def test_pack_size_not_whole_number(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 7, pack_size=2.5)

    def test_preferred_not_true_or_false(self):
        self.assert_refused(ValueError, TAP_SKU, ACME, 5.0, 7, preferred="yes")

    def test_second_preferred_supplier(self):
        self.assert_refused(
            ValueError, PIPE_SKU, DELTA, 4.80, 10, preferred=True)


if __name__ == "__main__":
    unittest.main()
