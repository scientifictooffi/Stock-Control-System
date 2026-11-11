import unittest
from stock_control.models import Batch, Product, Warehouse
from stock_control.movements.issuing import issue_stock
from stock_control.store import Store

def make_store():
    store = Store()
    store.warehouses["MAIN"] = Warehouse("MAIN", "Main warehouse")
    store.warehouses["NORTH"] = Warehouse("NORTH", "North warehouse")
    store.products["PIP-0001"] = Product(
        "PIP-0001", "Pipe", "Plumbing", 4.5, quantity=10,
        stock_by_warehouse={"MAIN": 10})
    store.products["TAP-0001"] = Product(
        "TAP-0001", "Tap", "Plumbing", 24.0, quantity=5,
        stock_by_warehouse={"MAIN": 5})
    store.batches = [
        Batch("B0001", "PIP-0001", "MAIN", 4, "2026-11-01", "2026-12-20"),
        Batch("B0002", "PIP-0001", "MAIN", 5, "2026-11-05", "2026-11-20"),
        Batch("B0003", "TAP-0001", "MAIN", 5, "2026-11-02", None),
    ]
    return store

class TestIssueStockConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        self.assertEqual(
            5, issue_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-11-11"))

    def test_iteration_1_negate_d9_needs_unbatched_stock(self):
        store = make_store()
        self.assertEqual(
            10, issue_stock(store, "PIP-0001", 10, "MAIN", "2026-11-11"))
        self.assertIn("no batch:1", store.movements[0].reason)

    def test_iteration_2_negate_d4_not_enough_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "PIP-0001", 11, "MAIN", "2026-11-11")

    def test_iteration_3_negate_d5_part_order(self):
        self.assertEqual(
            10, issue_stock(make_store(), "PIP-0001", 11, "MAIN",
                            "2026-11-11", True))

    def test_iteration_4_negate_d9_part_order_from_batches(self):
        self.assertEqual(
            5, issue_stock(make_store(), "TAP-0001", 8, "MAIN", "2026-11-11",
                           True))

    def test_iteration_5_negate_d6_no_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "TAP-0001", 8, "NORTH", "2026-11-11",
                        True)

    def test_iteration_6_negate_d3_warehouse(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "TAP-0001", 8, "EAST", "2026-11-11",
                        True)

    def test_iteration_7_negate_d2_quantity(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "TAP-0001", 0, "EAST", "2026-11-11",
                        True)

    def test_iteration_8_negate_d1_sku_missing(self):
        with self.assertRaises(KeyError):
            issue_stock(make_store(), "XYZ-9999", 0, "EAST", "2026-11-11",
                        True)


if __name__ == "__main__":
    unittest.main()
