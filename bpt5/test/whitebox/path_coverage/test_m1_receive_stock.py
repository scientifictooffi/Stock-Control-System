import unittest
from bpt5.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, START_QTY, TODAY, UNKNOWN_SKU, make_store,
    snapshot)
from stock_control.movements.receiving import receive_stock


class TestReceiveStockPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args):
        with self.assertRaises(error) as ctx:
            receive_stock(self.store, *args)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def assert_path_accepted(self, *args):
        result = receive_stock(self.store, *args)
        self.assertEqual(result, START_QTY + args[1])
        self.assertEqual(len(self.store.batches), 1)
        self.assertEqual(len(self.store.movements), 1)
        return result

    def test_path_1_unknown_product(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, 5, "MAIN", TODAY)

    def test_path_2_not_active(self):
        self.assert_path_refused(
            ValueError, "not active", ARCHIVED_SKU, 5, "MAIN", TODAY)

    def test_path_3_bad_quantity(self):
        self.assert_path_refused(
            ValueError, "quantity", ACTIVE_SKU, True, "MAIN", TODAY)

    def test_path_4_unknown_warehouse(self):
        self.assert_path_refused(
            ValueError, "warehouse", ACTIVE_SKU, 5, "EAST", TODAY)

    def test_path_5_bad_date(self):
        self.assert_path_refused(
            ValueError, "date must be", ACTIVE_SKU, 5, "MAIN", "7 Nov 2026")

    def test_path_5_bad_date_compact(self):
        self.assert_path_refused(
            ValueError, "date must be", ACTIVE_SKU, 5, "MAIN", "20261107")

    def test_path_6_success_no_use_by(self):
        self.assert_path_accepted(ACTIVE_SKU, 5, "MAIN", TODAY)
        self.assertIsNone(self.store.batches[0].use_by_date)

    def test_path_7_bad_use_by(self):
        self.assert_path_refused(
            ValueError, "use-by date must be",
            ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-99")

    def test_path_7_bad_use_by_compact(self):
        self.assert_path_refused(
            ValueError, "use-by date must be",
            ACTIVE_SKU, 5, "MAIN", TODAY, "20261201")

    def test_path_8_use_by_in_past(self):
        self.assert_path_refused(
            ValueError, "in the past",
            ACTIVE_SKU, 5, "MAIN", TODAY, "2026-01-01")

    def test_path_9_success(self):
        self.assert_path_accepted(ACTIVE_SKU, 5, "NORTH", TODAY, "2027-01-01")
        self.assertEqual(self.store.batches[0].use_by_date, "2027-01-01")


if __name__ == "__main__":
    unittest.main()
