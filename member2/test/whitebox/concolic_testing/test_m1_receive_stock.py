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


class TestReceiveStockConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        store = make_store()
        total = receive_stock(store, "PIP-0001", 5, "MAIN", "2026-11-07",
                              "2026-12-01")
        self.assertEqual(5, total)

    def test_iteration_1_negate_d8_use_by_before_date(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-11-07",
                          "2026-11-06")

    def test_iteration_2_negate_d7_use_by_not_valid(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-11-07",
                          "2026-13-01")

    def test_iteration_3_negate_d6_no_use_by(self):
        store = make_store()
        total = receive_stock(store, "PIP-0001", 5, "MAIN", "2026-11-07")
        self.assertEqual(5, total)
        self.assertIsNone(store.batches[0].use_by_date)

    def test_iteration_4_negate_d5_date(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "MAIN", "2026-02-30")

    def test_iteration_5_negate_d4_warehouse(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 5, "EAST", "2026-11-07")

    def test_iteration_6_negate_d3_quantity(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "PIP-0001", 0, "MAIN", "2026-11-07")

    def test_iteration_7_negate_d2_not_active(self):
        with self.assertRaises(ValueError):
            receive_stock(make_store(), "OLD-0001", 5, "MAIN", "2026-11-07")

    def test_iteration_8_negate_d1_sku_missing(self):
        with self.assertRaises(KeyError):
            receive_stock(make_store(), "TAP-0001", 5, "MAIN", "2026-11-07")


if __name__ == "__main__":
    unittest.main()
