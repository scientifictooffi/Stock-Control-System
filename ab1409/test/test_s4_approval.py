import unittest

from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order


class TestS4Approval(unittest.TestCase):

    def test_under_1000_auto_approves(self):
        store = make_store(total=999.99)
        self.assertEqual(
            approve_order(store, PO_ID, None).status,
            "sent"
        )

    def test_exactly_1000_requires_manager(self):
        store = make_store(total=1000)

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, None)

        self.assertEqual(store.purchase_orders[PO_ID].status, "draft")

        self.assertEqual(
            approve_order(store, PO_ID, "manager1").status,
            "sent"
        )

    def test_5000_requires_manager(self):
        store = make_store(total=5000)
        self.assertEqual(
            approve_order(store, PO_ID, "manager1").status,
            "sent"
        )

    def test_over_5000_requires_admin(self):
        store = make_store(total=5000.01)

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, "manager1")

        self.assertEqual(
            approve_order(store, PO_ID, "owner1").status,
            "sent"
        )

    def test_rejection_sets_rejected_status(self):
        store = make_store(total=2000)
        self.assertEqual(
            approve_order(
                store, PO_ID, "manager1", "reject"
            ).status,
            "rejected"
        )

    def test_unknown_order_raises_key_error(self):
        store = make_store()

        with self.assertRaises(KeyError):
            approve_order(store, "missing", None)

    def test_invalid_decision_raises_value_error(self):
        store = make_store()

        with self.assertRaises(ValueError):
            approve_order(store, PO_ID, None, "maybe")

    def test_inactive_manager_cannot_approve(self):
        store = make_store(total=2000)
        store.users["manager1"].active = False

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, "manager1")


if __name__ == "__main__":
    unittest.main()