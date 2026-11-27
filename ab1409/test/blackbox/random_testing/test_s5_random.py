import random
import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID, SKU_A, DATE
from stock_control.purchasing.receiving import receive_against_po


class TestS5RandomisedReceiving(unittest.TestCase):
    def test_random_partial_receipts_remain_partial(self):
        rng = random.Random(510)
        for quantity in [rng.randint(1, 9) for _ in range(30)]:
            store = make_store(status="sent")
            self.assertEqual(receive_against_po(store, PO_ID, {SKU_A: quantity}, "MAIN", DATE).status, "partially_received")

    def test_random_overdelivery_above_tolerance_is_rejected(self):
        rng = random.Random(511)
        for quantity in [rng.randint(22, 40) for _ in range(30)]:
            store = make_store(status="sent")
            store.purchase_orders[PO_ID].lines[0].quantity = 20
            with self.assertRaises(ValueError):
                receive_against_po(store, PO_ID, {SKU_A: quantity}, "MAIN", DATE)
