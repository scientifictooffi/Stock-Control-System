"""Seeded concrete tests that flip key S4 approval decisions."""
import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4ConcolicRuns(unittest.TestCase):
    def test_flip_at_1000_boundary(self):
        self.assertEqual(approve_order(make_store(total=999.99), PO_ID, None).status, "sent")
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=1000), PO_ID, None)

    def test_flip_at_5000_boundary(self):
        self.assertEqual(approve_order(make_store(total=5000), PO_ID, "manager1").status, "sent")
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=5000.01), PO_ID, "manager1")

    def test_flip_required_role(self):
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=6000), PO_ID, "manager1")
        self.assertEqual(approve_order(make_store(total=6000), PO_ID, "owner1").status, "sent")

if __name__ == "__main__":
    unittest.main()
