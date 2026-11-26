"""Checked-in representative tests derived from S4_Approval.tsl."""
import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4CategoryPartition(unittest.TestCase):
    def test_value_below_auto_threshold(self):
        self.assertEqual(approve_order(make_store(total=999.99), PO_ID, None).status, "sent")

    def test_exact_manager_threshold(self):
        self.assertEqual(approve_order(make_store(total=1000), PO_ID, "manager1").status, "sent")

    def test_middle_manager_partition(self):
        self.assertEqual(approve_order(make_store(total=2500), PO_ID, "manager1").status, "sent")

    def test_exact_upper_manager_threshold(self):
        self.assertEqual(approve_order(make_store(total=5000), PO_ID, "manager1").status, "sent")

    def test_admin_partition(self):
        with self.assertRaises(PermissionError):
            approve_order(make_store(total=5000.01), PO_ID, "manager1")
        self.assertEqual(approve_order(make_store(total=5000.01), PO_ID, "owner1").status, "sent")

    def test_unknown_order_partition(self):
        with self.assertRaises(KeyError):
            approve_order(make_store(), "missing", None)

    def test_invalid_decision_partition(self):
        with self.assertRaises(ValueError):
            approve_order(make_store(), PO_ID, None, "invalid")

if __name__ == "__main__":
    unittest.main()
