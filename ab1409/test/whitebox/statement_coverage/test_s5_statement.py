import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5StatementCoverage(unittest.TestCase):
    def test_receipt_updates_all_expected_records(self):
        store = make_store(status="sent")
        receive_against_po(store, PO_ID, {SKU_A: 10}, "MAIN", DATE)
        self.assertEqual(store.products[SKU_A].quantity, 20)
        self.assertEqual(store.products[SKU_A].stock_by_warehouse["MAIN"], 10)
        self.assertEqual(len(store.movements), 1)
        self.assertEqual(store.purchase_orders[PO_ID].status, "received")
