"""R1 login - white-box: concolic testing.

Start from one concrete input, record the path it takes, negate the last
decision on that path, solve for a new input and repeat (see
docs/research/R1_login.md for each iteration).
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_success(self):
        store = make_store()
        self.assertEqual("sam", login(store, "sam", "pass123").username)

    def test_iteration_1_negate_d4_wrong_password(self):
        with self.assertRaisesRegex(ValueError, "^wrong password$"):
            login(make_store(), "sam", "wrong")

    def test_iteration_2_negate_d5_reach_limit(self):
        store = make_store()
        store.users["sam"].failed_logins = 2
        with self.assertRaisesRegex(ValueError, "now locked"):
            login(store, "sam", "wrong")

    def test_iteration_3_negate_d3_inactive(self):
        with self.assertRaisesRegex(ValueError, "inactive"):
            login(make_store(), "lee", "pass123")

    def test_iteration_4_negate_d2_locked(self):
        with self.assertRaisesRegex(ValueError, "account is locked"):
            login(make_store(), "kim", "pass123")

    def test_iteration_5_negate_d1_unknown_user(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            login(make_store(), "nobody", "pass123")


if __name__ == "__main__":
    unittest.main()
