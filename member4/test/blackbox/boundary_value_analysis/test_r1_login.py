"""R1 login - black-box: boundary value analysis.

The boundary is the number of wrong tries before the lock (limit = 3).
Values tested: 0, 1, 2 (just below), 3 (on the limit), 4 (just above).
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


def wrong_tries(store, count):
    for _ in range(count):
        try:
            login(store, "sam", "wrong")
        except ValueError:
            pass


class TestLoginBoundaryValues(unittest.TestCase):

    def test_0_wrong_tries_can_log_in(self):
        store = make_store()
        self.assertIs(login(store, "sam", "pass123"), store.users["sam"])

    def test_1_wrong_try_not_locked(self):
        store = make_store()
        wrong_tries(store, 1)
        self.assertFalse(store.users["sam"].locked)
        self.assertEqual(1, store.users["sam"].failed_logins)

    def test_2_wrong_tries_still_can_log_in(self):
        store = make_store()
        wrong_tries(store, 2)
        self.assertFalse(store.users["sam"].locked)
        self.assertIs(login(store, "sam", "pass123"), store.users["sam"])

    def test_3_wrong_tries_locks_account(self):
        store = make_store()
        wrong_tries(store, 3)
        self.assertTrue(store.users["sam"].locked)
        with self.assertRaises(ValueError):
            login(store, "sam", "pass123")

    def test_4_wrong_tries_stays_locked_and_count_stops(self):
        store = make_store()
        wrong_tries(store, 4)
        self.assertTrue(store.users["sam"].locked)
        self.assertEqual(3, store.users["sam"].failed_logins)

    def test_correct_password_resets_count_to_0(self):
        store = make_store()
        wrong_tries(store, 2)
        login(store, "sam", "pass123")
        self.assertEqual(0, store.users["sam"].failed_logins)


if __name__ == "__main__":
    unittest.main()
