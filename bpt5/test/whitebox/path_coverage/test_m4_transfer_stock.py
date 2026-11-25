import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, TODAY, UNKNOWN_SKU, add_transfer, make_store,
    snapshot, stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def use_transfer(self, status):
        add_transfer(self.store, status)
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args):
        with self.assertRaises(error) as ctx:
            transfer_stock(self.store, *args)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def assert_path_changed(self, action, status):
        transfer = transfer_stock(self.store, None, None, None, None,
                                  action, "TR0001", "alex", TODAY)
        self.assertEqual(transfer.status, status)
        return transfer

    def test_path_1_unknown_product(self):
        self.assert_path_refused(
            KeyError, "does not exist", UNKNOWN_SKU, 1, "MAIN", "NORTH")

    def test_path_2_invalid_quantity(self):
        self.assert_path_refused(
            ValueError, "quantity", SKU, -1, "MAIN", "NORTH")

    def test_path_3_same_warehouse(self):
        self.assert_path_refused(
            ValueError, "different", SKU, 1, "MAIN", "MAIN")

    def test_path_4_unknown_warehouse(self):
        self.assert_path_refused(
            ValueError, "must exist", SKU, 1, "MAIN", "WEST")

    def test_path_5_not_enough_stock(self):
        self.assert_path_refused(
            ValueError, "not enough stock", SKU, MAIN_QTY + 1, "MAIN",
            "NORTH")

    def test_path_6_create(self):
        transfer = transfer_stock(self.store, SKU, 10, "MAIN", "NORTH",
                                  user="alex", date=TODAY)
        self.assertEqual(transfer.status, "pending")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 10)
        self.assertEqual(len(self.store.movements), 1)

    def test_path_7_invalid_action(self):
        self.use_transfer("pending")
        self.assert_path_refused(
            ValueError, "action", None, None, None, None, "remove",
            "TR0001")

    def test_path_8_unknown_transfer(self):
        self.assert_path_refused(
            KeyError, "does not exist", None, None, None, None, "cancel",
            "TR0001")

    def test_path_9_wrong_status(self):
        self.use_transfer("cancelled")
        self.assert_path_refused(
            ValueError, "cannot receive", None, None, None, None,
            "receive", "TR0001")

    def test_path_10_dispatch(self):
        self.use_transfer("pending")
        self.assert_path_changed("dispatch", "in transit")
        self.assertEqual(self.store.movements, [])

    def test_path_11_receive(self):
        self.use_transfer("in transit")
        self.assert_path_changed("receive", "received")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + 10)
        self.assertEqual(self.store.movements[-1].movement_type,
                         "transfer in")

    def test_path_12_cancel(self):
        self.use_transfer("pending")
        self.assert_path_changed("cancel", "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)
        self.assertEqual(self.store.movements[-1].movement_type,
                         "transfer cancel")


if __name__ == "__main__":
    unittest.main()
