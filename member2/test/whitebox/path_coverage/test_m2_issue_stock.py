import unittest
from member2.test.m2_fixtures import (
    MAIN_QTY, OTHER_SKU, SKU, TODAY, UNKNOWN_SKU, make_store, snapshot)
from stock_control.movements.issuing import issue_stock

class TestIssueStockPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args):
        with self.assertRaises(error) as ctx:
            issue_stock(self.store, *args)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def assert_path_issued(self, expected, reason, *args):
        self.assertEqual(issue_stock(self.store, *args), expected)
        self.assertEqual(self.store.movements[-1].reason, reason)

    def test_p1(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, 1, "MAIN", TODAY)

    def test_p2(self):
        self.assert_path_refused(
            ValueError, "quantity", SKU, True, "MAIN", TODAY)

    def test_p3(self):
        self.assert_path_refused(
            ValueError, "warehouse", SKU, 1, "EAST", TODAY)

    def test_p4(self):
        self.assert_path_refused(
            ValueError, "not enough stock", SKU, 20, "MAIN", TODAY)

    def test_p5(self):
        self.assert_path_refused(
            ValueError, "no stock", SKU, 3, "NORTH", TODAY, True)

    def test_p6a_full_issue_loop_breaks(self):
        self.assert_path_issued(
            3, "issued from B0002:3", SKU, 3, "MAIN", TODAY)

    def test_p6b_full_issue_loop_ends(self):
        self.assert_path_issued(
            9, "issued from B0002:3, B0001:4, B0003:2",
            SKU, 9, "MAIN", TODAY)

    def test_p7a_full_issue_no_batches(self):
        self.store.batches = []
        self.assert_path_issued(
            4, "issued from no batch:4", SKU, 4, "MAIN", TODAY)

    def test_p7b_full_issue_batches_then_unbatched(self):
        self.assert_path_issued(
            MAIN_QTY, "issued from B0002:3, B0001:4, B0003:2, no batch:1",
            SKU, MAIN_QTY, "MAIN", TODAY)

    def test_p8_part_order_all_from_batches(self):
        self.assert_path_issued(
            5, "issued from B0004:5", OTHER_SKU, 8, "MAIN", TODAY, True)

    def test_p9_part_order_batches_then_unbatched(self):
        self.assert_path_issued(
            MAIN_QTY, "issued from B0002:3, B0001:4, B0003:2, no batch:1",
            SKU, 25, "MAIN", TODAY, True)


if __name__ == "__main__":
    unittest.main()
