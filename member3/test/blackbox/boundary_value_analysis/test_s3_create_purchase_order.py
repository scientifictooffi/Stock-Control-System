import unittest
from member3.test.s3_fixtures import (
    ACME, DELTA, PIPE_SKU, TAP_SKU, TODAY, make_store, snapshot)
from stock_control.models import ProductSupplier
from stock_control.purchasing.orders import create_purchase_order


class TestQuantityBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def order(self, quantity):
        return create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, quantity)], TODAY)

    def test_quantity_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            self.order(-1)

    def test_quantity_zero_is_rejected(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            self.order(0)
        self.assertEqual(self.store, before)

    def test_quantity_one_is_accepted(self):
        self.assertEqual(self.order(1).lines[0].quantity, 1)

    def test_quantity_two_is_accepted(self):
        self.assertEqual(self.order(2).total_ex_vat, 24.00)

    def test_quantity_large_is_accepted(self):
        self.assertEqual(self.order(1_000_000).total_ex_vat, 12_000_000.00)


class TestNumberOfItemsBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_zero_items_is_rejected(self):
        with self.assertRaises(ValueError):
            create_purchase_order(self.store, DELTA, [], TODAY)

    def test_one_item_is_accepted(self):
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(len(order.lines), 1)

    def test_two_items_are_accepted(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 5), (TAP_SKU, 1)], TODAY)
        self.assertEqual(len(order.lines), 2)


class TestMinimumOrderBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_one_below_minimum_is_rejected(self):
        with self.assertRaises(ValueError):
            create_purchase_order(self.store, ACME, [(PIPE_SKU, 4)], TODAY)

    def test_penny_below_minimum_is_rejected(self):
        self.store.suppliers[DELTA].min_order_value = 12.01
        with self.assertRaises(ValueError):
            create_purchase_order(self.store, DELTA, [(PIPE_SKU, 1)], TODAY)

    def test_exactly_the_minimum_is_accepted(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 5)], TODAY)
        self.assertEqual(order.total_ex_vat, 50.00)

    def test_exactly_the_minimum_is_accepted_to_the_penny(self):
        self.store.suppliers[DELTA].min_order_value = 12.00
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(order.total_ex_vat, 12.00)

    def test_penny_above_minimum_is_accepted(self):
        self.store.suppliers[DELTA].min_order_value = 11.99
        order = create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], TODAY)
        self.assertEqual(order.total_ex_vat, 12.00)

    def test_minimum_is_checked_before_vat_is_added(self):
        # 4 pipes = 40.00 ex VAT = 48.00 inc VAT: both under 50
        # 4 pipes + 1 tap = 45.50 ex VAT = 54.60 inc VAT: refused,
        # because the ex-VAT total is under 50
        with self.assertRaises(ValueError):
            create_purchase_order(
                self.store, ACME, [(PIPE_SKU, 4), (TAP_SKU, 1)], TODAY)

    def test_minimum_met_by_several_lines(self):
        order = create_purchase_order(
            self.store, ACME, [(PIPE_SKU, 4), (TAP_SKU, 2)], TODAY)
        self.assertEqual(order.total_ex_vat, 51.00)

    def test_minimum_zero_accepts_a_penny_order(self):
        self.store.product_suppliers.append(
            ProductSupplier("TAP-0002", DELTA, 0.01, 3))
        order = create_purchase_order(
            self.store, DELTA, [(TAP_SKU, 1)], TODAY)
        self.assertEqual(order.total_ex_vat, 0.01)


class TestVatRoundingBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.store.product_suppliers.append(
            ProductSupplier("TAP-0002", DELTA, 0.01, 3))

    def vat_for(self, quantity):
        return create_purchase_order(
            self.store, DELTA, [(TAP_SKU, quantity)], TODAY)

    def test_one_penny_gives_one_penny_with_vat(self):
        self.assertEqual(self.vat_for(1).total_inc_vat, 0.01)

    def test_four_pennies_round_up_to_five(self):
        order = self.vat_for(4)
        self.assertEqual((order.total_ex_vat, order.total_inc_vat),
                         (0.04, 0.05))

    def test_five_pennies_give_six(self):
        self.assertEqual(self.vat_for(5).total_inc_vat, 0.06)

    def test_one_hundred_pennies_give_one_twenty(self):
        self.assertEqual(self.vat_for(100).total_inc_vat, 1.20)


class TestDateBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def order(self, day):
        return create_purchase_order(
            self.store, DELTA, [(PIPE_SKU, 1)], day)

    def test_leap_day_is_accepted(self):
        self.assertEqual(self.order("2028-02-29").created_date, "2028-02-29")

    def test_29_feb_in_non_leap_year_is_rejected(self):
        with self.assertRaises(ValueError):
            self.order("2026-02-29")

    def test_31_nov_is_rejected(self):
        with self.assertRaises(ValueError):
            self.order("2026-11-31")

    def test_30_nov_is_accepted(self):
        self.assertEqual(self.order("2026-11-30").created_date, "2026-11-30")

    def test_month_13_is_rejected(self):
        with self.assertRaises(ValueError):
            self.order("2026-13-01")

    def test_month_00_is_rejected(self):
        with self.assertRaises(ValueError):
            self.order("2026-00-10")

    def test_year_end_is_accepted(self):
        self.assertEqual(self.order("2026-12-31").created_date, "2026-12-31")


if __name__ == "__main__":
    unittest.main()
