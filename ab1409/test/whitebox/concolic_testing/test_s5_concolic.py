import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5ConcolicRuns(unittest.TestCase):
    def test_flip_partial_to_complete(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 9}, "MAIN", DATE).status, "partially_received")
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_flip_five_percent_allowance(self):
        accepted = make_store(status="sent")
        accepted.purchase_orders[PO_ID].lines[0].quantity = 20
        self.assertEqual(receive_against_po(accepted, PO_ID, {SKU_A: 21}, "MAIN", DATE).status, "received")
        rejected = make_store(status="sent")
        rejected.purchase_orders[PO_ID].lines[0].quantity = 20
        with self.assertRaises(ValueError):
            receive_against_po(rejected, PO_ID, {SKU_A: 22}, "MAIN", DATE)
