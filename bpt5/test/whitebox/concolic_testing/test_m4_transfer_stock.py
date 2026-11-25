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


class TestTransferStockConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_create(self):
        transfer = transfer_stock(make_store(), "PIP-0001", 5, "MAIN",
                                  "NORTH")
        self.assertEqual("pending", transfer.status)

    def test_iteration_1_negate_d6_not_enough(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 25, "MAIN", "NORTH")

    def test_iteration_2_negate_d5_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 25, "MAIN", "EAST")

    def test_iteration_3_negate_d4_same_warehouse(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 25, "MAIN", "MAIN")

    def test_iteration_4_negate_d3_quantity(self):
        with self.assertRaises(ValueError):
            transfer_stock(make_store(), "PIP-0001", 0, "MAIN", "MAIN")

    def test_iteration_5_negate_d2_product(self):
        with self.assertRaises(KeyError):
            transfer_stock(make_store(), "XYZ-9999", 0, "MAIN", "MAIN")

    def test_iteration_6_negate_d1_not_create(self):
        with self.assertRaises(KeyError):
            change(make_store(), "dispatch", None)

    def test_iteration_7_negate_d8_transfer_exists(self):
        self.assertEqual("in transit",
                         change(make_store("pending"), "dispatch").status)

    def test_iteration_8_negate_d10_not_dispatch(self):
        self.assertEqual("cancelled",
                         change(make_store("pending"), "cancel").status)

    def test_iteration_9_negate_d11_receive(self):
        self.assertEqual("received",
                         change(make_store("in transit"), "receive").status)

    def test_iteration_10_negate_d9_status_not_allowed(self):
        with self.assertRaises(ValueError):
            change(make_store("pending"), "receive")

    def test_iteration_11_negate_d7_bad_action(self):
        with self.assertRaises(ValueError):
            change(make_store("pending"), "lose")


if __name__ == "__main__":
    unittest.main()
