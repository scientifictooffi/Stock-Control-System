import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5RepresentativePaths(unittest.TestCase):
    def test_partial_receipt_path(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 1}, "MAIN", DATE).status, "partially_received")

    def test_complete_receipt_path(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_invalid_state_path(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="draft"), PO_ID, {SKU_A: 1}, "MAIN", DATE)
