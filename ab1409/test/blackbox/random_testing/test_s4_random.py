import random
import unittest
from ab1409.test.s456_fixtures import make_store, PO_ID
from stock_control.purchasing.approval import approve_order

class TestS4RandomisedAmounts(unittest.TestCase):
    def test_random_low_value_orders_auto_approve(self):
        rng = random.Random(406)
        for _ in range(40):
            amount = rng.uniform(0, 999.99)
            with self.subTest(amount=amount):
                self.assertEqual(approve_order(make_store(total=amount), PO_ID, None).status, "sent")

    def test_random_manager_range_accepts_manager(self):
        rng = random.Random(408)
        for _ in range(40):
            amount = rng.uniform(1000, 5000)
            with self.subTest(amount=amount):
                self.assertEqual(approve_order(make_store(total=amount), PO_ID, "manager1").status, "sent")

    def test_random_high_value_orders_reject_manager(self):
        rng = random.Random(407)
        for _ in range(40):
            amount = rng.uniform(5000.01, 100000)
            with self.subTest(amount=amount):
                with self.assertRaises(PermissionError):
                    approve_order(make_store(total=amount), PO_ID, "manager1")

if __name__ == "__main__":
    unittest.main()
