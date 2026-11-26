import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4RepresentativePaths(unittest.TestCase):
    def test_automatic_approval_path(self):
        self.assertEqual(approve_order(make_store(total=500), PO_ID, None).status, "sent")

    def test_manager_approval_path(self):
        self.assertEqual(approve_order(make_store(total=2500), PO_ID, "manager1").status, "sent")

    def test_admin_approval_path(self):
        self.assertEqual(approve_order(make_store(total=6000), PO_ID, "owner1").status, "sent")

    def test_rejection_path(self):
        self.assertEqual(approve_order(make_store(total=2500), PO_ID, "manager1", "reject").status, "rejected")

if __name__ == "__main__":
    unittest.main()
