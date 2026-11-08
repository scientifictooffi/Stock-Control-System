import unittest
from stock_control.models import Product, Warehouse
from stock_control.movements.receiving import receive_stock
from stock_control.store import Store


def make_store():
    store = Store()
    store.warehouses["MAIN"] = Warehouse("MAIN", "Main warehouse")
    store.products["PIP-0001"] = Product("PIP-0001", "Pipe", "Plumbing", 4.5)
    store.products["OLD-0001"] = Product("OLD-0001", "Old tap", "Plumbing",
                                         2.0, status="archived")
    return store


class TestReceiveStockSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_sku_not_in_products(self):
        with self.assertRaises(KeyError):
            receive_stock(make_store(), "TAP-0001", 5, "MAIN", "2026-11-07")

    def test_leaf_l2_pc_product_not_active(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "OLD-0001", 5, "MAIN", "2026-11-07")

    def test_leaf_l3_pc_quantity_not_positive_int(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 0, "MAIN", "2026-11-07")

    def test_leaf_l4_pc_warehouse_missing(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "EAST", "2026-11-07")

    def test_leaf_l5_pc_date_not_valid(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-02-30")

    def test_leaf_l6_pc_no_use_by(self):
        store = make_store()
        total = receive_stock(store, "PIP-0001", 5, "MAIN", "2026-11-07")
        self.assertEqual(5, total)
        self.assertEqual(5, store.products["PIP-0001"].stock_by_warehouse[
            "MAIN"])

    def test_leaf_l7_pc_use_by_not_valid(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-11-07",
                          "2026-13-01")

    def test_leaf_l8_pc_use_by_before_date(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-11-07",
                          "2026-11-06")

    def test_leaf_l9_pc_all_rules_hold(self):
        store = make_store()
        total = receive_stock(store, "PIP-0001", 5, "MAIN", "2026-11-07",
                              "2026-11-07")
        self.assertEqual(5, total)
        self.assertEqual("2026-11-07", store.batches[0].use_by_date)


if __name__ == "__main__":
    unittest.main()
