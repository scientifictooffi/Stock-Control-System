import unittest
from stock_control.models import Product, ProductSupplier, Supplier
from stock_control.purchasing.orders import create_purchase_order
from stock_control.store import Store

DAY = "2026-11-07"


def make_store():
    store = Store()
    for sku in ("PIP-0001", "TAP-0002", "BRK-0003"):
        store.products[sku] = Product(sku, sku, "Plumbing", 1.0)
    store.suppliers["SUP0001"] = Supplier(
        "SUP0001", "Acme", "a@acme.co", "01164960001", min_order_value=50.0)
    store.suppliers["SUP0002"] = Supplier(
        "SUP0002", "Sigma", "s@sigma.co", "01164960002", "suspended")
    store.product_suppliers.append(
        ProductSupplier("PIP-0001", "SUP0001", 10, 3))
    store.product_suppliers.append(
        ProductSupplier("TAP-0002", "SUP0001", 5, 3))
    return store


class TestCreatePurchaseOrderConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        order = create_purchase_order(
            make_store(), "SUP0001", [("PIP-0001", 6), ("TAP-0002", 2)], DAY)
        self.assertEqual(70.0, order.total_ex_vat)

    def test_iteration_1_negate_d9_total_below_minimum(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 1), ("TAP-0002", 1)],
                DAY)

    def test_iteration_2_negate_d8_second_item_duplicate(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 6), ("PIP-0001", 2)],
                DAY)

    def test_iteration_3_negate_d7_second_quantity_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 6), ("TAP-0002", 0)],
                DAY)

    def test_iteration_4_negate_d6_second_item_not_sold(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 6), ("BRK-0003", 2)],
                DAY)

    def test_iteration_5_negate_d5_second_item_not_a_pair(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 6), "TAP-0002"], DAY)

    def test_iteration_6_negate_d7_first_quantity_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 0), ("TAP-0002", 2)],
                DAY)

    def test_iteration_7_negate_d6_first_item_not_sold(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("BRK-0003", 3), ("TAP-0002", 2)],
                DAY)

    def test_iteration_8_negate_d5_first_item_not_a_pair(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [None, ("TAP-0002", 2)], DAY)

    def test_iteration_9_negate_d4_date_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 6), ("TAP-0002", 2)],
                "07-11-2026")

    def test_iteration_10_negate_d3_no_lines(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [], DAY)

    def test_iteration_11_negate_d2_supplier_not_active(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0002", [("PIP-0001", 6)], DAY)

    def test_iteration_12_negate_d1_supplier_unknown(self):
        with self.assertRaises(KeyError):
            create_purchase_order(
                make_store(), "SUP0042", [("PIP-0001", 6)], DAY)


if __name__ == "__main__":
    unittest.main()
