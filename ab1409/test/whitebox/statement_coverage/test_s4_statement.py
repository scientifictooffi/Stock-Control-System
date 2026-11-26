import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4StatementCoverage(unittest.TestCase):
    def test_automatic_approval_statements(self):
        self.assertEqual(approve_order(make_store(total=999), PO_ID, None).status, "sent")

    def test_manual_approval_statements(self):
        self.assertEqual(approve_order(make_store(total=1000), PO_ID, "manager1").status, "sent")

    def test_rejection_statements(self):
        self.assertEqual(approve_order(make_store(total=2000), PO_ID, "manager1", "reject").status, "rejected")

if __name__ == "__main__":
    unittest.main()
