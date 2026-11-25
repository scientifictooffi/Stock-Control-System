import unittest
from stock_control.models import Product, Transfer, Warehouse
from stock_control.movements.transfers import transfer_stock
from stock_control.store import Store


def make_store(status=None):
    store = Store()
    store.warehouses["MAIN"] = Warehouse("MAIN", "Main warehouse")
    store.warehouses["NORTH"] = Warehouse("NORTH", "North warehouse")
    store.products["PIP-0001"] = Product(
        "PIP-0001", "Pipe", "Plumbing", 4.5, quantity=20,
        stock_by_warehouse={"MAIN": 20})
    if status is not None:
        store.products["PIP-0001"].stock_by_warehouse["MAIN"] = 15
        store.transfers["TR0001"] = Transfer(
            "TR0001", "PIP-0001", 5, "MAIN", "NORTH", status)
    return store


def change(store, action, transfer_id="TR0001"):
    return transfer_stock(store, None, None, None, None, action,
                          transfer_id, "alex", "2026-11-23")


class TestTransferStockSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_unknown_sku(self):
        with self.assertRaises(KeyError):
            transfer_stock(make_store(), "XYZ-9999", 5, "MAIN", "NORTH")

    def test_leaf_l2_pc_quantity_not_positive(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 0, "MAIN", "NORTH")

    def test_leaf_l3_pc_same_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 5, "MAIN", "MAIN")

    def test_leaf_l4_pc_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 5, "MAIN", "EAST")

    def test_leaf_l5_pc_not_enough_stock(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 21, "MAIN", "NORTH")

    def test_leaf_l6_pc_create_rules_hold(self):
        store = make_store()
        transfer = transfer_stock(store, "PIP-0001", 5, "MAIN", "NORTH")
        self.assertEqual("pending", transfer.status)
        self.assertEqual(15, store.products["PIP-0001"].stock_by_warehouse[
            "MAIN"])

    def test_leaf_l7_pc_bad_action(self):
        with self.assertRaises(ValueError):
            change(make_store("pending"), "return")

    def test_leaf_l8_pc_unknown_transfer(self):
        with self.assertRaises(KeyError):
            change(make_store(), "dispatch")

    def test_leaf_l9_pc_status_not_allowed(self):
        with self.assertRaises(ValueError):
            change(make_store("received"), "cancel")

    def test_leaf_l10_pc_dispatch(self):
        self.assertEqual("in transit",
                         change(make_store("pending"), "dispatch").status)

    def test_leaf_l11_pc_receive(self):
        store = make_store("in transit")
        self.assertEqual("received", change(store, "receive").status)
        self.assertEqual(5, store.products["PIP-0001"].stock_by_warehouse[
            "NORTH"])

    def test_leaf_l12_pc_cancel(self):
        store = make_store("in transit")
        self.assertEqual("cancelled", change(store, "cancel").status)
        self.assertEqual(20, store.products["PIP-0001"].stock_by_warehouse[
            "MAIN"])


if __name__ == "__main__":
    unittest.main()
