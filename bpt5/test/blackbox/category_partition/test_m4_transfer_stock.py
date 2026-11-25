import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, TODAY, UNKNOWN_SKU, add_transfer, make_store,
    snapshot, stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockCategoryPartition(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def refused(self, error, *args):
        before = snapshot(self.store)
        with self.assertRaises(error):
            transfer_stock(self.store, *args)
        self.assertEqual(self.store, before)

    def change(self, status, action):
        add_transfer(self.store, status)
        return transfer_stock(self.store, None, None, None, None, action,
                              "TR0001", "alex", TODAY)

    def change_refused(self, status, action):
        add_transfer(self.store, status)
        self.refused(ValueError, None, None, None, None, action, "TR0001")

    # error and single frames
    def test_frame_01_unknown_action_error(self):
        self.refused(ValueError, SKU, 1, "MAIN", "NORTH", "move")

    def test_frame_02_unknown_product_error(self):
        self.refused(KeyError, UNKNOWN_SKU, 1, "MAIN", "NORTH")

    def test_frame_03_quantity_equal_to_stock_single(self):
        transfer_stock(self.store, SKU, MAIN_QTY, "MAIN", "NORTH")
        self.assertEqual(stock(self.store, "MAIN"), 0)

    def test_frame_04_quantity_above_stock_error(self):
        self.refused(ValueError, SKU, MAIN_QTY + 1, "MAIN", "NORTH")

    def test_frame_05_quantity_zero_or_negative_error(self):
        self.refused(ValueError, SKU, -4, "MAIN", "NORTH")

    def test_frame_06_quantity_not_whole_number_error(self):
        self.refused(ValueError, SKU, 1.5, "MAIN", "NORTH")

    def test_frame_07_same_warehouse_error(self):
        self.refused(ValueError, SKU, 1, "NORTH", "NORTH")

    def test_frame_08_from_warehouse_unknown_error(self):
        self.refused(ValueError, SKU, 1, "EAST", "NORTH")

    def test_frame_09_to_warehouse_unknown_error(self):
        self.refused(ValueError, SKU, 1, "MAIN", "EAST")

    def test_frame_10_unknown_transfer_error(self):
        self.refused(KeyError, None, None, None, None, "receive", "TR0404")

    # normal frames
    def test_frame_11_create(self):
        transfer = transfer_stock(self.store, SKU, 10, "MAIN", "NORTH")
        self.assertEqual(transfer.status, "pending")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 10)

    def test_frame_12_dispatch_pending(self):
        self.assertEqual(self.change("pending", "dispatch").status,
                         "in transit")

    def test_frame_13_dispatch_in_transit(self):
        self.change_refused("in transit", "dispatch")

    def test_frame_14_dispatch_received(self):
        self.change_refused("received", "dispatch")

    def test_frame_15_dispatch_cancelled(self):
        self.change_refused("cancelled", "dispatch")

    def test_frame_16_receive_pending(self):
        self.change_refused("pending", "receive")

    def test_frame_17_receive_in_transit(self):
        self.assertEqual(self.change("in transit", "receive").status,
                         "received")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + 10)

    def test_frame_18_receive_received(self):
        self.change_refused("received", "receive")

    def test_frame_19_receive_cancelled(self):
        self.change_refused("cancelled", "receive")

    def test_frame_20_cancel_pending(self):
        self.assertEqual(self.change("pending", "cancel").status,
                         "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)

    def test_frame_21_cancel_in_transit(self):
        self.assertEqual(self.change("in transit", "cancel").status,
                         "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)

    def test_frame_22_cancel_received(self):
        self.change_refused("received", "cancel")

    def test_frame_23_cancel_cancelled(self):
        self.change_refused("cancelled", "cancel")


if __name__ == "__main__":
    unittest.main()
