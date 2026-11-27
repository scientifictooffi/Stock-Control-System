import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5CategoryPartition(unittest.TestCase):
    def test_sent_known_sku_valid_quantity(self):
        self.assertEqual(receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 2}, "MAIN", DATE).status, "partially_received")

    def test_empty_received_map_rejected(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="sent"), PO_ID, {}, "MAIN", DATE)

    def test_unknown_warehouse_rejected(self):
        with self.assertRaises(KeyError):
            receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 1}, "UNKNOWN", DATE)

    def test_invalid_date_rejected(self):
        with self.assertRaises(ValueError):
            receive_against_po(make_store(status="sent"), PO_ID, {SKU_A: 1}, "MAIN", "not-a-date")
