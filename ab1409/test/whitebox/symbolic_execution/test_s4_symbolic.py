"""Concrete representatives for S4 symbolic path conditions."""
import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4SymbolicPathRepresentatives(unittest.TestCase):
    def test_pc_amount_below_1000(self):
        self.assertEqual(approve_order(make_store(total=999.99), PO_ID, None).status, "sent")

    def test_pc_1000_to_5000_inclusive(self):
        self.assertEqual(approve_order(make_store(total=1000), PO_ID, "manager1").status, "sent")

    def test_pc_amount_above_5000(self):
        self.assertEqual(approve_order(make_store(total=5000.01), PO_ID, "owner1").status, "sent")

    def test_pc_wrong_role(self):
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=2500), PO_ID, "buyer1")

if __name__ == "__main__":
    unittest.main()
