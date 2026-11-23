import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, NORTH_QTY, SKU, TODAY, UNKNOWN_SKU, add_transfer, make_store,
    stock)
from stock_control.movements.transfers import transfer_stock


class TestTransferStockStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def change(self, action, transfer_id="TR0001"):
        return transfer_stock(self.store, None, None, None, None, action,
                              transfer_id, "alex", TODAY)

    def test_statement_raise_unknown_product(self):
        with self.assertRaises(KeyError):
            transfer_stock(self.store, UNKNOWN_SKU, 1, "MAIN", "NORTH")

    def test_statement_raise_quantity(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 0, "MAIN", "NORTH")

    def test_statement_raise_same_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 1, "NORTH", "NORTH")

    def test_statement_raise_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, 1, "MAIN", "EAST")

    def test_statement_raise_not_enough_stock(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, SKU, MAIN_QTY + 1, "MAIN", "NORTH")

    def test_statements_create(self):
        transfer = transfer_stock(self.store, SKU, 10, "MAIN", "NORTH",
                                  date=TODAY)
        self.assertEqual(transfer.status, "pending")
        self.assertIs(self.store.transfers["TR0001"], transfer)

    def test_statement_raise_action(self):
        with self.assertRaises(ValueError):
            self.change("move")

    def test_statement_raise_unknown_transfer(self):
        with self.assertRaises(KeyError):
            self.change("dispatch")

    def test_statement_raise_wrong_status(self):
        add_transfer(self.store, "received")
        with self.assertRaises(ValueError):
            self.change("cancel")

    def test_statements_dispatch(self):
        add_transfer(self.store, "pending")
        self.assertEqual(self.change("dispatch").status, "in transit")

    def test_statements_receive(self):
        add_transfer(self.store, "in transit")
        self.assertEqual(self.change("receive").status, "received")
        self.assertEqual(stock(self.store, "NORTH"), NORTH_QTY + 10)

    def test_statements_cancel(self):
        add_transfer(self.store, "pending")
        self.assertEqual(self.change("cancel").status, "cancelled")
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY)


if __name__ == "__main__":
    unittest.main()
