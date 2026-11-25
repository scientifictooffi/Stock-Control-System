import unittest
from bpt5.test.m1_fixtures import (
    ACTIVE_SKU, START_QTY, TODAY, make_store, snapshot)
from stock_control.movements.receiving import receive_stock


class TestQuantityBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_quantity_minus_one_is_rejected(self):
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, -1, "MAIN", TODAY)

    def test_quantity_zero_is_rejected(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            receive_stock(self.store, ACTIVE_SKU, 0, "MAIN", TODAY)
        self.assertEqual(self.store, before)

    def test_quantity_one_is_accepted(self):
        self.assertEqual(
            receive_stock(self.store, ACTIVE_SKU, 1, "MAIN", TODAY),
            START_QTY + 1)

    def test_quantity_two_is_accepted(self):
        self.assertEqual(
            receive_stock(self.store, ACTIVE_SKU, 2, "MAIN", TODAY),
            START_QTY + 2)

    def test_quantity_large_is_accepted(self):
        self.assertEqual(
            receive_stock(self.store, ACTIVE_SKU, 1_000_000, "MAIN", TODAY),
            START_QTY + 1_000_000)


class TestUseByBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def receive(self, date, use_by):
        return receive_stock(self.store, ACTIVE_SKU, 1, "MAIN", date, use_by)

    def test_use_by_one_day_before_is_rejected(self):
        with self.assertRaises(ValueError):
            self.receive(TODAY, "2026-11-06")

    def test_use_by_same_day_is_accepted(self):
        self.assertEqual(self.receive(TODAY, TODAY), START_QTY + 1)

    def test_use_by_one_day_after_is_accepted(self):
        self.assertEqual(self.receive(TODAY, "2026-11-08"), START_QTY + 1)

    def test_use_by_end_of_previous_month_is_rejected(self):
        with self.assertRaises(ValueError):
            self.receive("2026-12-01", "2026-11-30")

    def test_use_by_start_of_next_year_is_accepted(self):
        self.assertEqual(self.receive("2026-12-31", "2027-01-01"),
                         START_QTY + 1)

    def test_use_by_end_of_previous_year_is_rejected(self):
        with self.assertRaises(ValueError):
            self.receive("2027-01-01", "2026-12-31")

    def test_use_by_leap_day_is_accepted(self):
        self.assertEqual(self.receive("2028-02-28", "2028-02-29"),
                         START_QTY + 1)

    def test_use_by_29_feb_non_leap_year_is_rejected(self):
        with self.assertRaises(ValueError):
            self.receive("2026-02-28", "2026-02-29")


if __name__ == "__main__":
    unittest.main()
