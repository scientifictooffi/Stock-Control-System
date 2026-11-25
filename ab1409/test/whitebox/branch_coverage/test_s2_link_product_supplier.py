import unittest
from ab1409.test.s2_fixtures import (
    ACME, ARCHIVED_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, make_store_with_preferred)
from stock_control.purchasing.suppliers import link_product_supplier


class TestLinkProductSupplierBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def refused(self, error, *args, **kwargs):
        with self.assertRaises(error):
            link_product_supplier(self.store, *args, **kwargs)

    def test_branch_product_missing_true(self):
        self.refused(KeyError, UNKNOWN_SKU, ACME, 5.0, 7)

    def test_branch_product_not_active_true(self):
        self.refused(ValueError, ARCHIVED_SKU, ACME, 5.0, 7)

    def test_branch_supplier_missing_true(self):
        self.refused(KeyError, PIPE_SKU, UNKNOWN_ID, 5.0, 7)

    def test_branch_supplier_not_active_true(self):
        self.refused(ValueError, PIPE_SKU, SUSPENDED_ID, 5.0, 7)

    def test_branch_price_not_number_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, "5", 7)

    def test_branch_price_is_bool_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, True, 7)

    def test_branch_price_not_finite_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, float("inf"), 7)

    def test_branch_price_not_positive_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, -2.0, 7)

    def test_branch_lead_time_not_whole_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 2.5)

    def test_branch_lead_time_too_small_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 0)

    def test_branch_lead_time_too_big_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 91)

    def test_branch_pack_size_not_whole_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 7, pack_size="2")

    def test_branch_pack_size_too_small_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 7, pack_size=0)

    def test_branch_preferred_not_bool_true(self):
        self.refused(ValueError, PIPE_SKU, ACME, 5.0, 7, preferred=None)

    def test_branch_preferred_conflict_true(self):
        self.store = make_store_with_preferred()
        self.refused(ValueError, PIPE_SKU, DELTA, 4.0, 7, preferred=True)

    def test_branch_preferred_false_skips_conflict_check(self):
        self.store = make_store_with_preferred()
        link = link_product_supplier(self.store, PIPE_SKU, DELTA, 4.0, 7)
        self.assertFalse(link.preferred)

    def test_branch_preferred_true_no_conflict_false(self):
        link = link_product_supplier(
            self.store, PIPE_SKU, ACME, 5.0, 7, preferred=True)
        self.assertTrue(link.preferred)

    def test_branch_preferred_true_same_supplier_false(self):
        self.store = make_store_with_preferred()
        link_product_supplier(self.store, PIPE_SKU, ACME, 5.5, 7, True)
        self.assertEqual(self.store.products[PIPE_SKU].preferred_supplier,
                         ACME)

    def test_branch_link_missing_true_creates(self):
        link_product_supplier(self.store, TAP_SKU, DELTA, 9.0, 7)
        self.assertEqual(len(self.store.product_suppliers), 1)

    def test_branch_link_exists_false_updates(self):
        link_product_supplier(self.store, TAP_SKU, DELTA, 9.0, 7)
        link_product_supplier(self.store, TAP_SKU, DELTA, 8.0, 5)
        self.assertEqual(len(self.store.product_suppliers), 1)
        self.assertEqual(self.store.product_suppliers[0].price, 8.0)

    def test_branch_preferred_list_empty_gives_none(self):
        link_product_supplier(self.store, TAP_SKU, DELTA, 9.0, 7)
        self.assertIsNone(self.store.products[TAP_SKU].preferred_supplier)

    def test_branch_preferred_list_not_empty_gives_id(self):
        link_product_supplier(self.store, TAP_SKU, DELTA, 9.0, 7, True)
        self.assertEqual(self.store.products[TAP_SKU].preferred_supplier,
                         DELTA)


if __name__ == "__main__":
    unittest.main()
