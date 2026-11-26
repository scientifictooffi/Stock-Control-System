import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4BranchCoverage(unittest.TestCase):
    def test_amount_threshold_branches(self):
        approve_order(make_store(total=999), PO_ID, None)
        approve_order(make_store(total=1000), PO_ID, "manager1")
        approve_order(make_store(total=5000.01), PO_ID, "owner1")

    def test_approval_and_rejection_branches(self):
        self.assertEqual(approve_order(make_store(total=2000), PO_ID, "manager1", "approve").status, "sent")
        self.assertEqual(approve_order(make_store(total=2000), PO_ID, "manager1", "reject").status, "rejected")

    def test_authorisation_failure_branch(self):
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=2000), PO_ID, "buyer1")

if __name__ == "__main__":
    unittest.main()
