import unittest

from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order


class TestS4ApprovalBoundaries(unittest.TestCase):

    def test_just_below_1000_auto_approves(self):
        store = make_store(total=999.99)

        self.assertEqual(
            approve_order(store, PO_ID, None).status,
            "sent"
        )

    def test_exactly_1000_requires_manager(self):
        store = make_store(total=1000)

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, None)

    def test_just_above_1000_requires_manager(self):
        store = make_store(total=1000.01)

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, None)

        self.assertEqual(
            approve_order(store, PO_ID, "manager1").status,
            "sent"
        )

    def test_exactly_5000_accepts_manager(self):
        store = make_store(total=5000)

        self.assertEqual(
            approve_order(store, PO_ID, "manager1").status,
            "sent"
        )

    def test_just_above_5000_requires_admin(self):
        store = make_store(total=5000.01)

        with self.assertRaises(PermissionError):
            approve_order(store, PO_ID, "manager1")

        self.assertEqual(
            approve_order(store, PO_ID, "owner1").status,
            "sent"
        )


if __name__ == "__main__":
    unittest.main()