import unittest
from stock_control.models import Product, User, Warehouse
from stock_control.movements.adjustments import adjust_stock
from stock_control.store import Store


def make_store():
    store = Store()
    store.warehouses["MAIN"] = Warehouse("MAIN", "Main warehouse")
    store.products["PIP-0001"] = Product(
        "PIP-0001", "Pipe", "Plumbing", 4.5, cost=6.0, quantity=50,
        stock_by_warehouse={"MAIN": 50})
    store.users["kim"] = User("kim", "pass123", "manager")
    return store


class TestAdjustStockSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_unknown_sku(self):
        with self.assertRaises(KeyError):
            adjust_stock(make_store(), "XYZ-9999", -2, "damaged", "MAIN",
                         "2026-11-14")

    def test_leaf_l2_pc_bad_reason(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -2, "stolen", "MAIN",
                         "2026-11-14")

    def test_leaf_l3_pc_change_zero(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", 0, "damaged", "MAIN",
                         "2026-11-14")

    def test_leaf_l4_pc_unknown_warehouse(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -2, "damaged", "EAST",
                         "2026-11-14")

    def test_leaf_l5_pc_below_zero(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -51, "damaged", "MAIN",
                         "2026-11-14", "kim")

    def test_leaf_l6_pc_all_rules_hold(self):
        store = make_store()
        self.assertEqual(48, adjust_stock(store, "PIP-0001", -2, "damaged",
                                          "MAIN", "2026-11-14"))
        self.assertEqual(48, store.products["PIP-0001"].quantity)

    def test_leaf_l7_pc_big_change_not_approved(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -20, "lost", "MAIN",
                         "2026-11-14")

    def test_leaf_l8_pc_big_change_approved(self):
        store = make_store()
        self.assertEqual(30, adjust_stock(store, "PIP-0001", -20, "lost",
                                          "MAIN", "2026-11-14", "kim"))
        self.assertEqual(-20, store.movements[0].quantity)


if __name__ == "__main__":
    unittest.main()
