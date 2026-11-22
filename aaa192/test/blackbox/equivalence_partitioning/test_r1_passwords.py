"""R1 password hashing - black-box: equivalence partitioning.

Input classes taken from the rules of hash_password and hash_for_user:
  password: non-empty string (valid) | empty string (invalid) |
            not a string (invalid)
  salt:     not given (valid) | non-empty hex string (valid) |
            empty string (invalid) | not hex (invalid) | not a string
            (invalid)
  user:     stored hashed (valid) | unknown (invalid) |
            stored in plain text (invalid) | stored value not salt$hash
            (invalid)
One test per class, plus the full login flow with the hashed demo data.
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.auth import login
from stock_control.reporting.passwords import hash_for_user, hash_password
from stock_control.seed import demo_store


class TestHashPasswordEquivalenceClasses(unittest.TestCase):

    def test_valid_password_with_given_salt(self):
        self.assertEqual(hash_password(PASSWORD, SALT),
                         expected_hash(PASSWORD))

    def test_valid_password_without_salt(self):
        stored = hash_password(PASSWORD)
        salt = stored.split("$")[0]
        self.assertEqual(stored, expected_hash(PASSWORD, salt))
        self.assertNotIn(PASSWORD, stored)

    def test_invalid_password_empty(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)

    def test_invalid_password_not_a_string(self):
        with self.assertRaises(ValueError):
            hash_password(123, SALT)

    def test_invalid_salt_empty(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_invalid_salt_not_hex(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "xyz")

    def test_invalid_salt_not_a_string(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, 99)


class TestHashForUserEquivalenceClasses(unittest.TestCase):

    def test_valid_hashed_user(self):
        self.assertEqual(hash_for_user(make_store(), "sam", PASSWORD),
                         expected_hash(PASSWORD))

    def test_invalid_unknown_user(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)

    def test_invalid_empty_password(self):
        self.assertEqual(hash_for_user(make_store(), "sam", ""), "")

    def test_invalid_plain_stored_password(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_invalid_stored_value_not_salt_hash(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)


class TestLoginWithHashedDemoUsers(unittest.TestCase):

    def test_demo_passwords_are_not_stored_in_plain_text(self):
        store = demo_store()
        for name, plain in (("admin", "admin123"), ("manager", "manager123"),
                            ("clerk", "clerk123")):
            self.assertNotEqual(store.users[name].password, plain)
            self.assertNotIn(plain, store.users[name].password)

    def test_each_demo_user_has_its_own_salt(self):
        store = demo_store()
        salts = {user.password.split("$")[0]
                 for user in store.users.values()}
        self.assertEqual(len(salts), len(store.users))

    def test_correct_password_logs_in(self):
        store = demo_store()
        typed = hash_for_user(store, "admin", "admin123")
        self.assertIs(login(store, "admin", typed), store.users["admin"])

    def test_wrong_password_counts_a_failed_try(self):
        store = demo_store()
        typed = hash_for_user(store, "admin", "wrong")
        with self.assertRaises(ValueError):
            login(store, "admin", typed)
        self.assertEqual(store.users["admin"].failed_logins, 1)

    def test_three_wrong_passwords_lock_the_account(self):
        store = demo_store()
        for _ in range(3):
            with self.assertRaises(ValueError):
                login(store, "clerk", hash_for_user(store, "clerk", "bad"))
        self.assertTrue(store.users["clerk"].locked)


if __name__ == "__main__":
    unittest.main()
