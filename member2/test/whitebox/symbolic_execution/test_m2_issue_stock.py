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


class TestIssueStockSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_sku_not_in_products(self):
        with self.assertRaises(KeyError):
            issue_stock(make_store(), "XYZ-9999", 1, "MAIN", "2026-11-11")

    def test_leaf_l2_pc_quantity_not_positive_int(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "PIP-0001", 0, "MAIN", "2026-11-11")

    def test_leaf_l3_pc_warehouse_missing(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "PIP-0001", 1, "EAST", "2026-11-11")

    def test_leaf_l4_pc_not_enough_and_no_part_order(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "PIP-0001", 11, "MAIN", "2026-11-11")

    def test_leaf_l5_pc_part_order_but_no_stock(self):
        with self.assertRaises(ValueError):
            issue_stock(make_store(), "PIP-0001", 1, "NORTH", "2026-11-11",
                        True)

    def test_leaf_l6_pc_full_issue_from_batches(self):
        store = make_store()
        self.assertEqual(
            5, issue_stock(store, "PIP-0001", 5, "MAIN", "2026-11-11"))
        self.assertEqual(0, store.batches[1].quantity)
        self.assertEqual(4, store.batches[0].quantity)

    def test_leaf_l7_pc_full_issue_needs_unbatched_stock(self):
        store = make_store()
        self.assertEqual(
            10, issue_stock(store, "PIP-0001", 10, "MAIN", "2026-11-11"))
        self.assertIn("no batch:1", store.movements[0].reason)

    def test_leaf_l8_pc_part_order_from_batches(self):
        store = make_store()
        self.assertEqual(
            5, issue_stock(store, "TAP-0001", 8, "MAIN", "2026-11-11", True))
        self.assertEqual(0, store.products["TAP-0001"].quantity)

    def test_leaf_l9_pc_part_order_needs_unbatched_stock(self):
        store = make_store()
        self.assertEqual(
            10, issue_stock(store, "PIP-0001", 12, "MAIN", "2026-11-11",
                            True))
        self.assertEqual(0, store.products["PIP-0001"].stock_by_warehouse[
            "MAIN"])


if __name__ == "__main__":
    unittest.main()
