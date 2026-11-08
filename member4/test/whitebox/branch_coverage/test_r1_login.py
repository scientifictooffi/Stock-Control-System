"""R1 login - white-box: branch coverage.

Decisions in login():
  D1 user is None          D2 user.locked          D3 not user.active
  D4 password is wrong     D5 failed_logins >= 3
Each decision is made True once and False once.
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginBranchCoverage(unittest.TestCase):

    def test_d1_true(self):
        with self.assertRaises(ValueError):
            login(make_store(), "nobody", "pass123")

    def test_d1_false_d2_true(self):
        with self.assertRaises(ValueError):
            login(make_store(), "kim", "pass123")

    def test_d2_false_d3_true(self):
        with self.assertRaises(ValueError):
            login(make_store(), "lee", "pass123")

    def test_d3_false_d4_true_d5_false(self):
        store = make_store()
        with self.assertRaises(ValueError):
            login(store, "sam", "wrong")
        self.assertFalse(store.users["sam"].locked)

    def test_d4_true_d5_true(self):
        store = make_store()
        store.users["sam"].failed_logins = 2
        with self.assertRaises(ValueError):
            login(store, "sam", "wrong")
        self.assertTrue(store.users["sam"].locked)

    def test_d4_false(self):
        store = make_store()
        self.assertIs(login(store, "sam", "pass123"), store.users["sam"])


if __name__ == "__main__":
    unittest.main()
