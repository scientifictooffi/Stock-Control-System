import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4EquivalencePartitions(unittest.TestCase):
    def test_automatic_approval_group(self):
        self.assertEqual(approve_order(make_store(total=500), PO_ID, None).status, "sent")

    def test_manager_approval_group(self):
        self.assertEqual(approve_order(make_store(total=2500), PO_ID, "manager1").status, "sent")

    def test_admin_approval_group(self):
        self.assertEqual(approve_order(make_store(total=6000), PO_ID, "owner1").status, "sent")

    def test_wrong_role_group(self):
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=2500), PO_ID, "buyer1")

    def test_locked_approver_group(self):
        store = make_store(total=2500)
        store.users["manager1"].locked = True
        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, "manager1")

if __name__ == "__main__":
    unittest.main()
