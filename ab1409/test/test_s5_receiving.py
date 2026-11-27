import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5Receiving(unittest.TestCase):
    def sent_store(self):
        return make_store(status="sent")

    def test_partial_delivery_updates_line_stock_and_movement(self):
        store = self.sent_store()
        po = receive_against_po(store, PO_ID, {SKU_A: 4}, "MAIN", DATE, "manager1")
        self.assertEqual(po.status, "partially_received")
        self.assertEqual(po.lines[0].received, 4)
        self.assertEqual(store.products[SKU_A].quantity, 14)
        self.assertEqual(len(store.movements), 1)

    def test_full_delivery_closes_order(self):
        store = self.sent_store()
        self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_exact_five_percent_extra_is_accepted(self):
        store = self.sent_store()
        store.purchase_orders[PO_ID].lines[0].quantity = 20
        self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: 21}, "MAIN", DATE).status, "received")

    def test_more_than_five_percent_extra_is_rejected_atomically(self):
        store = self.sent_store()
        store.purchase_orders[PO_ID].lines[0].quantity = 20
        before = store.products[SKU_A].quantity
        with self.assertRaises(ValueError):
            receive_against_po(store, PO_ID, {SKU_A: 22}, "MAIN", DATE)
        self.assertEqual(store.products[SKU_A].quantity, before)
        self.assertEqual(store.movements, [])

    def test_order_must_be_sent(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="draft"), PO_ID, {SKU_A: 1}, "MAIN", DATE)

    def test_unknown_order_raises_key_error(self):
        with self.assertRaises(KeyError):
            receive_against_po(self.sent_store(), "missing", {SKU_A: 1}, "MAIN", DATE)

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            receive_against_po(self.sent_store(), PO_ID, {SKU_A: 0}, "MAIN", DATE)

    def test_unknown_sku_rejected_without_partial_mutation(self):
        store = self.sent_store()
        with self.assertRaises(ValueError):
            receive_against_po(store, PO_ID, {SKU_A: 1, "BAD": 1}, "MAIN", DATE)
        self.assertEqual(store.products[SKU_A].quantity, 10)
        self.assertEqual(store.movements, [])

    def test_partially_received_order_can_receive_remainder(self):
        store = self.sent_store()
        receive_against_po(store, PO_ID, {SKU_A: 4}, "MAIN", DATE)
        self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: 6}, "MAIN", DATE).status, "received")


if __name__ == "__main__":
    unittest.main()
