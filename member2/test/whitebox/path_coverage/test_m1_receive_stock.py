import unittest
from member2.test.m1_fixtures import (
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

    def test_p1(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, 5, "MAIN", TODAY)

    def test_p2(self):
        self.assert_path_refused(
            ValueError, "not active", ARCHIVED_SKU, 5, "MAIN", TODAY)

    def test_p3(self):
        self.assert_path_refused(
            ValueError, "quantity", ACTIVE_SKU, True, "MAIN", TODAY)

    def test_p4(self):
        self.assert_path_refused(
            ValueError, "warehouse", ACTIVE_SKU, 5, "EAST", TODAY)

    def test_p5(self):
        self.assert_path_refused(
            ValueError, "date must be", ACTIVE_SKU, 5, "MAIN", "7 Nov 2026")

    def test_p5b_compact_date(self):
        self.assert_path_refused(
            ValueError, "date must be", ACTIVE_SKU, 5, "MAIN", "20261107")

    def test_p6(self):
        self.assert_path_accepted(ACTIVE_SKU, 5, "MAIN", TODAY)
        self.assertIsNone(self.store.batches[0].use_by_date)

    def test_p7(self):
        self.assert_path_refused(
            ValueError, "use-by date must be",
            ACTIVE_SKU, 5, "MAIN", TODAY, "2026-11-99")

    def test_p7b_compact_use_by(self):
        self.assert_path_refused(
            ValueError, "use-by date must be",
            ACTIVE_SKU, 5, "MAIN", TODAY, "20261201")

    def test_p8(self):
        self.assert_path_refused(
            ValueError, "in the past",
            ACTIVE_SKU, 5, "MAIN", TODAY, "2026-01-01")

    def test_p9(self):
        self.assert_path_accepted(ACTIVE_SKU, 5, "NORTH", TODAY, "2027-01-01")
        self.assertEqual(self.store.batches[0].use_by_date, "2027-01-01")


if __name__ == "__main__":
    unittest.main()
