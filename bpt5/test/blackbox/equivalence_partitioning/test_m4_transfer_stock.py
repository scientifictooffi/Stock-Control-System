import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, TODAY, UNKNOWN_SKU, add_transfer, make_store,
    snapshot, stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockEquivalencePartitioning(unittest.TestCase):
    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args, **kwargs):
        with self.assertRaises(error):
            transfer_stock(self.store, *args, **kwargs)
        self.assertEqual(self.store, self.before)

    def use_transfer(self, status):
        add_transfer(self.store, status)
        self.before = snapshot(self.store)

    def change(self, action):
        return transfer_stock(self.store, None, None, None, None, action,
                              "TR0001", "alex", TODAY)

    # valid classes
    def test_valid_class_create(self):
        transfer = transfer_stock(self.store, SKU, 10, "MAIN", "NORTH",
                                  user="alex", date=TODAY)
        self.assertEqual(
            (transfer.transfer_id, transfer.status, transfer.quantity),
            ("TR0001", "pending", 10))
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 10)
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY)
        self.assertEqual(self.store.products[SKU].quantity,
                         MAIN_QTY + NORTH_QTY)

    def test_valid_class_create_saved_in_history(self):
        transfer_stock(self.store, SKU, 10, "MAIN", "NORTH", user="alex",
                       date=TODAY)
        movement = self.store.movements[-1]
        self.assertEqual(
            (movement.sku, movement.movement_type, movement.quantity,
             movement.warehouse, movement.date, movement.user),
            (SKU, "transfer out", 10, "MAIN", TODAY, "alex"))

    def test_valid_class_dispatch_pending(self):
        self.use_transfer("pending")
        self.assertEqual(self.change("dispatch").status, "in transit")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY)

    def test_valid_class_receive_in_transit(self):
        self.use_transfer("in transit")
        self.assertEqual(self.change("receive").status, "received")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + 10)
        self.assertEqual(self.store.movements[-1].movement_type,
                         "transfer in")

    def test_valid_class_cancel_pending(self):
        self.use_transfer("pending")
        self.assertEqual(self.change("cancel").status, "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)

    def test_valid_class_cancel_in_transit(self):
        self.use_transfer("in transit")
        self.assertEqual(self.change("cancel").status, "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY)

    # invalid classes for create
    def test_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, 1, "MAIN", "NORTH")

    def test_quantity_zero(self):
        self.assert_refused(ValueError, SKU, 0, "MAIN", "NORTH")

    def test_quantity_negative(self):
        self.assert_refused(ValueError, SKU, -3, "MAIN", "NORTH")

    def test_quantity_not_whole_number(self):
        self.assert_refused(ValueError, SKU, 2.5, "MAIN", "NORTH")

    def test_quantity_bool(self):
        self.assert_refused(ValueError, SKU, True, "MAIN", "NORTH")

    def test_same_warehouse(self):
        self.assert_refused(ValueError, SKU, 1, "MAIN", "MAIN")

    def test_unknown_from_warehouse(self):
        self.assert_refused(ValueError, SKU, 1, "EAST", "NORTH")

    def test_unknown_to_warehouse(self):
        self.assert_refused(ValueError, SKU, 1, "MAIN", "EAST")

    def test_not_enough_stock(self):
        self.assert_refused(ValueError, SKU, 6, "NORTH", "MAIN")

    # invalid classes for status changes
    def test_invalid_action(self):
        self.use_transfer("pending")
        self.assert_refused(ValueError, None, None, None, None, "ship",
                            "TR0001")

    def test_unknown_transfer(self):
        self.use_transfer("pending")
        self.assert_refused(KeyError, None, None, None, None, "dispatch",
                            "TR9999")

    def test_receive_pending(self):
        self.use_transfer("pending")
        self.assert_refused(ValueError, None, None, None, None, "receive",
                            "TR0001")

    def test_dispatch_in_transit(self):
        self.use_transfer("in transit")
        self.assert_refused(ValueError, None, None, None, None, "dispatch",
                            "TR0001")

    def test_cancel_received(self):
        self.use_transfer("received")
        self.assert_refused(ValueError, None, None, None, None, "cancel",
                            "TR0001")

    def test_dispatch_cancelled(self):
        self.use_transfer("cancelled")
        self.assert_refused(ValueError, None, None, None, None, "dispatch",
                            "TR0001")


if __name__ == "__main__":
    unittest.main()
