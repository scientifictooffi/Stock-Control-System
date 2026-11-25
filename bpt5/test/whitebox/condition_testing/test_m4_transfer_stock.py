import unittest
from bpt5.test.m4_fixtures import (
    MAIN_QTY, SKU, UNKNOWN_SKU, add_transfer, make_store, stock)
from stock_control.movements.transfers import transfer_stock

D9_TABLE = [
    ("dispatch", "pending", "in transit"),
    ("dispatch", "in transit", None),
    ("dispatch", "received", None),
    ("dispatch", "cancelled", None),
    ("receive", "pending", None),
    ("receive", "in transit", "received"),
    ("receive", "received", None),
    ("receive", "cancelled", None),
    ("cancel", "pending", "cancelled"),
    ("cancel", "in transit", "cancelled"),
    ("cancel", "received", None),
    ("cancel", "cancelled", None),
]


class TestTransferStockConditionTesting(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def create(self, quantity=1, source="MAIN", target="NORTH", sku=SKU):
        return transfer_stock(self.store, sku, quantity, source, target)

    # D3 truth table
    def test_d3_fff_whole_positive(self):
        self.create(5)
        self.assertEqual(stock(self.store, "MAIN"), MAIN_QTY - 5)

    def test_d3_fft_zero(self):
        with self.assertRaises(ValueError):
            self.create(0)

    def test_d3_ftf_true(self):
        with self.assertRaises(ValueError):
            self.create(True)

    def test_d3_ftt_false(self):
        with self.assertRaises(ValueError):
            self.create(False)

    def test_d3_tff_positive_float(self):
        with self.assertRaises(ValueError):
            self.create(2.5)

    def test_d3_tft_negative_float(self):
        with self.assertRaises(ValueError):
            self.create(-1.5)

    # D5 truth table
    def test_d5_ff_both_exist(self):
        self.assertEqual(self.create().status, "pending")

    def test_d5_ft_to_unknown(self):
        with self.assertRaises(ValueError):
            self.create(target="EAST")

    def test_d5_tf_from_unknown(self):
        with self.assertRaises(ValueError):
            self.create(source="EAST")

    def test_d5_tt_both_unknown(self):
        with self.assertRaises(ValueError):
            self.create(source="EAST", target="WEST")

    # simple conditions, true and false
    def test_d2_product_unknown_true(self):
        with self.assertRaises(KeyError):
            self.create(sku=UNKNOWN_SKU)

    def test_d4_same_warehouse_true(self):
        with self.assertRaises(ValueError):
            self.create(target="MAIN")

    def test_d6_above_stock_true(self):
        with self.assertRaises(ValueError):
            self.create(MAIN_QTY + 1)

    def test_d6_above_stock_false_at_limit(self):
        self.create(MAIN_QTY)
        self.assertEqual(stock(self.store, "MAIN"), 0)

    def test_d7_unknown_action_true(self):
        with self.assertRaises(ValueError):
            transfer_stock(self.store, None, None, None, None, "ship",
                           "TR0001")

    def test_d8_unknown_transfer_true(self):
        with self.assertRaises(KeyError):
            transfer_stock(self.store, None, None, None, None, "cancel",
                           "TR0001")

    # D9 x D10 x D11: every action with every status
    def test_d9_every_action_and_status(self):
        for action, status, result in D9_TABLE:
            with self.subTest(action=action, status=status):
                store = add_transfer(make_store(), status)
                if result is None:
                    with self.assertRaises(ValueError):
                        transfer_stock(store, None, None, None, None,
                                       action, "TR0001")
                    self.assertEqual(store.transfers["TR0001"].status,
                                     status)
                else:
                    transfer = transfer_stock(store, None, None, None, None,
                                              action, "TR0001")
                    self.assertEqual(transfer.status, result)


if __name__ == "__main__":
    unittest.main()
