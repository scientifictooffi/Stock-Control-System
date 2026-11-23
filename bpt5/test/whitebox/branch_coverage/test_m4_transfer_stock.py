import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, UNKNOWN_SKU, add_transfer, make_store, stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def change(self, action, transfer_id="TR0001"):
        return transfer_stock(self.store, None, None, None, None, action,
                              transfer_id)

    def test_branch_d2_product_true(self):
        with self.assertRaises(KeyError):
            transfer_stock(self.store, UNKNOWN_SKU, 1, "MAIN", "NORTH")

    def test_branch_d3_quantity_true(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, False, "MAIN", "NORTH")

    def test_branch_d4_same_warehouse_true(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 1, "MAIN", "MAIN")

    def test_branch_d5_warehouse_true(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 1, "SOUTH", "NORTH")

    def test_branch_d6_not_enough_true(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, NORTH_QTY + 1, "NORTH", "MAIN")

    def test_branch_d1_true_d2_to_d6_false_create(self):
        transfer_stock(self.store, SKU, 5, "MAIN", "NORTH")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 5)

    def test_branch_d1_false_d7_true(self):
        with self.assertRaises(ValueError):
            self.change("deliver")

    def test_branch_d8_true(self):
        with self.assertRaises(KeyError):
            self.change("receive", "TR0042")

    def test_branch_d9_true(self):
        add_transfer(self.store, "pending")
        with self.assertRaises(ValueError):
            self.change("receive")

    def test_branch_d10_true_dispatch(self):
        add_transfer(self.store, "pending")
        self.assertEqual(self.change("dispatch").status, "in transit")

    def test_branch_d10_false_d11_true_receive(self):
        add_transfer(self.store, "in transit")
        self.assertEqual(self.change("receive").status, "received")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + 10)

    def test_branch_d10_false_d11_false_cancel(self):
        add_transfer(self.store, "in transit")
        self.assertEqual(self.change("cancel").status, "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)


if __name__ == "__main__":
    unittest.main()
