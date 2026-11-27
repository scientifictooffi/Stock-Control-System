import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5EquivalencePartitions(unittest.TestCase):
    def test_partial_delivery_partition(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 3}, "MAIN", DATE).status, "partially_received")

    def test_complete_delivery_partition(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 10}, "MAIN", DATE).status, "received")

    def test_wrong_order_state_partition(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="draft"), PO_ID, {SKU_A: 3}, "MAIN", DATE)

    def test_invalid_sku_partition(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="sent"), PO_ID, {"UNKNOWN": 1}, "MAIN", DATE)
