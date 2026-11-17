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


class TestCreatePurchaseOrderSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_supplier_unknown(self):
        with self.assertRaises(KeyError):
            create_purchase_order(make_store(), "SUP0009", [("PIP-0001", 5)],
                                  DAY)

    def test_leaf_l2_pc_supplier_not_active(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0002", [("PIP-0001", 5)],
                                  DAY)

    def test_leaf_l3_pc_no_lines(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [], DAY)

    def test_leaf_l4_pc_date_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [("PIP-0001", 5)],
                                  "2026-02-30")

    def test_leaf_l5_pc_first_item_not_a_pair(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", ["PIP-0001"], DAY)

    def test_leaf_l6_pc_first_item_not_sold(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [("BRK-0003", 5)],
                                  DAY)

    def test_leaf_l7_pc_first_quantity_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [("PIP-0001", 0)],
                                  DAY)

    def test_leaf_l8_pc_n1_below_minimum(self):
        with self.assertRaises(ValueError):
            create_purchase_order(make_store(), "SUP0001", [("PIP-0001", 4)],
                                  DAY)

    def test_leaf_l9_pc_n1_success(self):
        order = create_purchase_order(
            make_store(), "SUP0001", [("PIP-0001", 5)], DAY)
        self.assertEqual(50.0, order.total_ex_vat)
        self.assertEqual(60.0, order.total_inc_vat)

    def test_leaf_l10_pc_second_item_not_a_pair(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 5), "TAP-0002"], DAY)

    def test_leaf_l11_pc_second_item_not_sold(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 5), ("BRK-0003", 1)],
                DAY)

    def test_leaf_l12_pc_second_quantity_invalid(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 5), ("TAP-0002", -1)],
                DAY)

    def test_leaf_l13_pc_second_item_duplicate(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 5), ("PIP-0001", 5)],
                DAY)

    def test_leaf_l14_pc_n2_below_minimum(self):
        with self.assertRaises(ValueError):
            create_purchase_order(
                make_store(), "SUP0001", [("PIP-0001", 1), ("TAP-0002", 1)],
                DAY)

    def test_leaf_l15_pc_n2_success(self):
        order = create_purchase_order(
            make_store(), "SUP0001", [("PIP-0001", 6), ("TAP-0002", 2)], DAY)
        self.assertEqual(70.0, order.total_ex_vat)
        self.assertEqual(84.0, order.total_inc_vat)


if __name__ == "__main__":
    unittest.main()
