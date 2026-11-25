import unittest
from ab1409.test.s2_fixtures import (
    ACME, PIPE_SKU, make_store, make_store_with_preferred, snapshot)
from stock_control.purchasing.suppliers import link_product_supplier


class TestPriceBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_price_minus_one_penny_is_rejected(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, -0.01, 7)

    def test_price_zero_is_rejected(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, 0, 7)
        self.assertEqual(self.store, before)

    def test_price_zero_float_is_rejected(self):
        with self.assertRaises(ValueError):
            link_product_supplier(self.store, PIPE_SKU, ACME, 0.0, 7)

    def test_price_one_penny_is_accepted(self):
        link = link_product_supplier(self.store, PIPE_SKU, ACME, 0.01, 7)
        self.assertEqual(link.price, 0.01)

    def test_price_two_pennies_is_accepted(self):
        link = link_product_supplier(self.store, PIPE_SKU, ACME, 0.02, 7)
        self.assertEqual(link.price, 0.02)

    def test_price_very_large_is_accepted(self):
        link = link_product_supplier(self.store, PIPE_SKU, ACME, 1e9, 7)
        self.assertEqual(link.price, 1e9)


class TestDeliveryTimeBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def link(self, days):
        return link_product_supplier(self.store, PIPE_SKU, ACME, 5.0, days)

    def test_0_days_is_rejected(self):
        with self.assertRaises(ValueError):
            self.link(0)

    def test_minus_1_day_is_rejected(self):
        with self.assertRaises(ValueError):
            self.link(-1)

    def test_1_day_is_accepted(self):
        self.assertEqual(self.link(1).lead_time_days, 1)

    def test_2_days_is_accepted(self):
        self.assertEqual(self.link(2).lead_time_days, 2)

    def test_89_days_is_accepted(self):
        self.assertEqual(self.link(89).lead_time_days, 89)

    def test_90_days_is_accepted(self):
        self.assertEqual(self.link(90).lead_time_days, 90)

    def test_91_days_is_rejected(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            self.link(91)
        self.assertEqual(self.store, before)

    def test_half_a_day_is_rejected(self):
        with self.assertRaises(ValueError):
            self.link(0.5)


class TestPackSizeBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def link(self, size):
        return link_product_supplier(
            self.store, PIPE_SKU, ACME, 5.0, 7, pack_size=size)

    def test_pack_size_0_is_rejected(self):
        with self.assertRaises(ValueError):
            self.link(0)

    def test_pack_size_1_is_accepted(self):
        self.assertEqual(self.link(1).pack_size, 1)

    def test_pack_size_2_is_accepted(self):
        self.assertEqual(self.link(2).pack_size, 2)


class TestPreferredBoundary(unittest.TestCase):

    def test_first_preferred_supplier_is_accepted(self):
        store = make_store()
        link = link_product_supplier(
            store, PIPE_SKU, ACME, 5.0, 7, preferred=True)
        self.assertTrue(link.preferred)

    def test_second_preferred_supplier_is_rejected(self):
        store = make_store_with_preferred()
        with self.assertRaises(ValueError):
            link_product_supplier(
                store, PIPE_SKU, "SUP0002", 4.0, 7, preferred=True)

    def test_second_preferred_supplier_accepted_after_first_is_removed(self):
        store = make_store_with_preferred()
        link_product_supplier(
            store, PIPE_SKU, ACME, 5.0, 3, preferred=False)
        link = link_product_supplier(
            store, PIPE_SKU, "SUP0002", 4.0, 7, preferred=True)
        self.assertTrue(link.preferred)

    def test_one_preferred_supplier_after_many_saves(self):
        store = make_store_with_preferred()
        for _ in range(3):
            link_product_supplier(
                store, PIPE_SKU, ACME, 5.0, 3, preferred=True)
        self.assertEqual(
            sum(1 for x in store.product_suppliers if x.preferred), 1)


if __name__ == "__main__":
    unittest.main()
