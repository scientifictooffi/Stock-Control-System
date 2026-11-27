import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5ReceivingBoundaries(unittest.TestCase):
    def test_exact_order_quantity_completes_order(self):
        store = make_store(status="sent")
        self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_exactly_105_percent_is_accepted(self):
        store = make_store(status="sent")
        store.purchase_orders[PO_ID].lines[0].quantity = 20
        self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: 21}, "MAIN", DATE).status, "received")

    def test_above_105_percent_is_rejected(self):
        store = make_store(status="sent")
        store.purchase_orders[PO_ID].lines[0].quantity = 20
        with self.assertRaises(ValueError):
            receive_against_po(store, PO_ID, {SKU_A: 22}, "MAIN", DATE)
