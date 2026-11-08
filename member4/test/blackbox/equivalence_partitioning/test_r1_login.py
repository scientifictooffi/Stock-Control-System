"""R1 login - black-box: equivalence partitioning.

Input classes taken from the four rules:
  username: exists (valid) | does not exist (invalid)
  account:  active and unlocked (valid) | locked (invalid) | inactive (invalid)
  password: correct (valid) | wrong (invalid)
One test per class.
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginEquivalencePartitioning(unittest.TestCase):

    def test_valid_class_all_rules_pass(self):
        store = make_store()
        user = login(store, "sam", "pass123")
        self.assertIs(user, store.users["sam"])

    def test_invalid_username_does_not_exist(self):
        with self.assertRaises(ValueError):
            login(make_store(), "nobody", "pass123")

    def test_invalid_username_empty(self):
        with self.assertRaises(ValueError):
            login(make_store(), "", "pass123")

    def test_invalid_password_wrong(self):
        with self.assertRaises(ValueError):
            login(make_store(), "sam", "wrong")

    def test_invalid_password_empty(self):
        with self.assertRaises(ValueError):
            login(make_store(), "sam", "")

    def test_invalid_account_locked(self):
        with self.assertRaises(ValueError):
            login(make_store(), "kim", "pass123")

    def test_invalid_account_inactive(self):
        with self.assertRaises(ValueError):
            login(make_store(), "lee", "pass123")


if __name__ == "__main__":
    unittest.main()
