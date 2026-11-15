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


class TestAdjustStockConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        self.assertEqual(48, adjust_stock(make_store(), "PIP-0001", -2,
                                          "damaged", "MAIN", "2026-11-14"))

    def test_iteration_1_negate_d6_big_change(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -20, "damaged", "MAIN",
                         "2026-11-14")

    def test_iteration_2_negate_d7_approved(self):
        self.assertEqual(30, adjust_stock(make_store(), "PIP-0001", -20,
                                          "damaged", "MAIN", "2026-11-14",
                                          "kim"))

    def test_iteration_3_negate_d5_below_zero(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -60, "damaged", "MAIN",
                         "2026-11-14", "kim")

    def test_iteration_4_negate_d4_warehouse(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", -60, "damaged", "EAST",
                         "2026-11-14", "kim")

    def test_iteration_5_negate_d3_change(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", 0, "damaged", "EAST",
                         "2026-11-14", "kim")

    def test_iteration_6_negate_d2_reason(self):
        with self.assertRaises(ValueError):
            adjust_stock(make_store(), "PIP-0001", 0, "stolen", "EAST",
                         "2026-11-14", "kim")

    def test_iteration_7_negate_d1_product(self):
        with self.assertRaises(KeyError):
            adjust_stock(make_store(), "XYZ-9999", 0, "stolen", "EAST",
                         "2026-11-14", "kim")


if __name__ == "__main__":
    unittest.main()
