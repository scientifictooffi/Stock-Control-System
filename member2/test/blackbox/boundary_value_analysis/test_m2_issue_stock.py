import unittest
from member2.test.m2_fixtures import (
    MAIN_QTY, SKU, TODAY, batch, make_store, snapshot)
from stock_control.models import Batch
from stock_control.movements.issuing import issue_stock

class TestQuantityBoundary(unittest.TestCase):
    def setUp(self):
        self.store = make_store()

    def stock_left(self):
        return self.store.products[SKU].stock_by_warehouse["MAIN"]

    def test_quantity_zero_refused(self):
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, 0, "MAIN", TODAY)

    def test_quantity_one_accepted(self):
        self.assertEqual(issue_stock(self.store, SKU, 1, "MAIN", TODAY), 1)

    def test_quantity_stock_minus_one_accepted(self):
        issue_stock(self.store, SKU, MAIN_QTY - 1, "MAIN", TODAY)
        self.assertEqual(self.stock_left(), 1)

    def test_quantity_equal_to_stock_leaves_zero(self):
        issue_stock(self.store, SKU, MAIN_QTY, "MAIN", TODAY)
        self.assertEqual(self.stock_left(), 0)

    def test_quantity_stock_plus_one_refused(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            issue_stock(self.store, SKU, MAIN_QTY + 1, "MAIN", TODAY)
        self.assertEqual(self.store, before)

    def test_quantity_stock_plus_one_part_order_issues_stock(self):
        self.assertEqual(
            issue_stock(self.store, SKU, MAIN_QTY + 1, "MAIN", TODAY, True),
            MAIN_QTY)
        self.assertEqual(self.stock_left(), 0)


class TestBatchBoundary(unittest.TestCase):
    def setUp(self):
        self.store = make_store()

    def test_exactly_first_batch_empties_it_only(self):
        issue_stock(self.store, SKU, 3, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0002").quantity, 0)
        self.assertEqual(batch(self.store, "B0001").quantity, 4)

    def test_one_more_than_first_batch_moves_to_next(self):
        issue_stock(self.store, SKU, 4, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0002").quantity, 0)
        self.assertEqual(batch(self.store, "B0001").quantity, 3)

    def test_all_batched_stock_uses_no_unbatched_stock(self):
        issue_stock(self.store, SKU, 9, "MAIN", TODAY)
        self.assertNotIn("no batch", self.store.movements[-1].reason)

    def test_one_more_than_batched_stock_uses_unbatched_stock(self):
        issue_stock(self.store, SKU, 10, "MAIN", TODAY)
        self.assertIn("no batch:1", self.store.movements[-1].reason)


class TestUseByBoundary(unittest.TestCase):
    def setUp(self):
        self.store = make_store()
        self.store.batches = [
            Batch("B0010", SKU, "MAIN", 2, "2026-11-03", "2026-11-21"),
            Batch("B0011", SKU, "MAIN", 2, "2026-11-01", "2026-11-21"),
            Batch("B0012", SKU, "MAIN", 2, "2026-10-01", "2026-11-20"),
        ]

    def test_use_by_one_day_earlier_goes_first(self):
        issue_stock(self.store, SKU, 2, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0012").quantity, 0)

    def test_same_use_by_earlier_arrival_goes_first(self):
        issue_stock(self.store, SKU, 4, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0011").quantity, 0)
        self.assertEqual(batch(self.store, "B0010").quantity, 2)


if __name__ == "__main__":
    unittest.main()
