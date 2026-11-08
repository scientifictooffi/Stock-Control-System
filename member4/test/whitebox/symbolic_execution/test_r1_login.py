"""R1 login - white-box: symbolic execution.

One test per leaf of the symbolic execution tree in
docs/research/R1_login.md, using the solution of that leaf's
path condition (PC).
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_user_missing(self):
        with self.assertRaises(ValueError):
            login(make_store(), "nobody", "pass123")

    def test_leaf_l2_pc_locked(self):
        with self.assertRaises(ValueError):
            login(make_store(), "kim", "pass123")

    def test_leaf_l3_pc_inactive(self):
        with self.assertRaises(ValueError):
            login(make_store(), "lee", "pass123")

    def test_leaf_l4_pc_wrong_and_f_plus_1_at_least_3(self):
        store = make_store()
        store.users["sam"].failed_logins = 2
        with self.assertRaises(ValueError):
            login(store, "sam", "wrong")
        self.assertTrue(store.users["sam"].locked)

    def test_leaf_l5_pc_wrong_and_f_plus_1_below_3(self):
        store = make_store()
        with self.assertRaises(ValueError):
            login(store, "sam", "wrong")
        self.assertEqual(1, store.users["sam"].failed_logins)

    def test_leaf_l6_pc_password_correct(self):
        store = make_store()
        store.users["sam"].failed_logins = 1
        user = login(store, "sam", "pass123")
        self.assertEqual(0, user.failed_logins)


if __name__ == "__main__":
    unittest.main()
