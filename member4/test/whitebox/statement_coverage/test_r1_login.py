"""R1 login - white-box: statement coverage.

Four tests run every statement in login() at least once
(each raise, the lock line, the reset line and the return).
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginStatementCoverage(unittest.TestCase):

    def test_statements_unknown_user_raise(self):
        with self.assertRaises(ValueError):
            login(make_store(), "nobody", "pass123")

    def test_statements_locked_and_inactive_raises(self):
        with self.assertRaises(ValueError):
            login(make_store(), "kim", "pass123")
        with self.assertRaises(ValueError):
            login(make_store(), "lee", "pass123")

    def test_statements_wrong_password_then_lock(self):
        store = make_store()
        for _ in range(3):
            with self.assertRaises(ValueError):
                login(store, "sam", "wrong")
        self.assertTrue(store.users["sam"].locked)

    def test_statements_success_reset_and_return(self):
        store = make_store()
        self.assertIs(login(store, "sam", "pass123"), store.users["sam"])


if __name__ == "__main__":
    unittest.main()
