import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5SymbolicPathRepresentatives(unittest.TestCase):
    def test_pc_received_less_than_ordered(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 1}, "MAIN", DATE).status, "partially_received")

    def test_pc_received_reaches_ordered(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_pc_exceeds_five_percent(self):
        store = make_store(status="sent")
        store.purchase_orders[PO_ID].lines[0].quantity = 20
        with self.assertRaises(ValueError):
            receive_against_po(store, PO_ID, {SKU_A: 22}, "MAIN", DATE)
