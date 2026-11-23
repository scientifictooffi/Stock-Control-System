import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, TODAY, make_store, stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockBoundaryValues(unittest.TestCase):
    def setUp(self):
        self.store = make_store()

    def test_quantity_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 0, "MAIN", "NORTH", date=TODAY)

    def test_quantity_one_is_accepted(self):
        transfer_stock(self.store, SKU, 1, "MAIN", "NORTH", date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 1)

    def test_quantity_two_is_accepted(self):
        transfer_stock(self.store, SKU, 2, "MAIN", "NORTH", date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 2)

    # quantity: upper boundary is the stock at the sending site
    def test_quantity_one_below_stock_is_accepted(self):
        transfer_stock(self.store, SKU, MAIN_QTY - 1, "MAIN", "NORTH",
                       date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), 1)

    def test_quantity_equal_to_stock_is_accepted(self):
        transfer_stock(self.store, SKU, MAIN_QTY, "MAIN", "NORTH",
                       date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), 0)

    def test_quantity_one_above_stock_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, MAIN_QTY + 1, "MAIN", "NORTH",
                           date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)

    # random low, mid-range and random high values (Lecture 8)
    def test_random_low_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, -7, "MAIN", "NORTH", date=TODAY)

    def test_mid_range_quantity_is_accepted(self):
        transfer_stock(self.store, SKU, 25, "MAIN", "NORTH", date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 25)

    def test_random_high_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 500, "MAIN", "NORTH",
                           date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)

    # sending site with no stock at all
    def test_empty_sending_site_is_rejected(self):
        self.store.products[SKU].stock_by_warehouse.pop("NORTH")
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 1, "NORTH", "MAIN", date=TODAY)

    # stock taken by an open transfer is no longer available
    def test_second_transfer_up_to_what_is_left_is_accepted(self):
        transfer_stock(self.store, SKU, 40, "MAIN", "NORTH", date=TODAY)
        transfer_stock(self.store, SKU, 10, "MAIN", "NORTH", date=TODAY)
        self.assertEqual(stock(self.store, "MAIN"), 0)

    def test_second_transfer_one_more_than_left_is_rejected(self):
        transfer_stock(self.store, SKU, 40, "MAIN", "NORTH", date=TODAY)
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 11, "MAIN", "NORTH", date=TODAY)

    # whole transfer round trip at the upper boundary
    def test_full_stock_received_at_other_site(self):
        transfer_stock(self.store, SKU, MAIN_QTY, "MAIN", "NORTH")
        transfer_stock(self.store, None, None, None, None, "dispatch",
                       "TR0001")
        transfer_stock(self.store, None, None, None, None, "receive",
                       "TR0001")
        self.assertEqual(stock(self.store, "MAIN"), 0)
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + MAIN_QTY)

    def test_full_stock_cancelled_returns_all(self):
        transfer_stock(self.store, SKU, MAIN_QTY, "MAIN", "NORTH")
        transfer_stock(self.store, None, None, None, None, "cancel",
                       "TR0001")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)


if __name__ == "__main__":
    unittest.main()
