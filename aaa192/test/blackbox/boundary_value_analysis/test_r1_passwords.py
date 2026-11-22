"""R1 password hashing - black-box: boundary value analysis.

Boundaries from the rules:
  password length: 0 (invalid) | 1 (smallest valid) | long (valid)
  salt length:     0 hex digits (invalid) | 1 hex digit (odd, invalid) |
                   2 hex digits (one byte, smallest valid)
  typed password:  exactly the stored one | one character different |
                   different only in letter case
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.auth import login
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestHashPasswordBoundaries(unittest.TestCase):

    def test_password_length_0_refused(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)

    def test_password_length_1_accepted(self):
        self.assertEqual(hash_password("x", SALT), expected_hash("x"))

    def test_long_password_accepted(self):
        long_password = "p" * 1000
        self.assertEqual(hash_password(long_password, SALT),
                         expected_hash(long_password))

    def test_salt_0_hex_digits_refused(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_salt_1_hex_digit_refused(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "a")

    def test_salt_2_hex_digits_accepted(self):
        self.assertEqual(hash_password(PASSWORD, "ab"),
                         expected_hash(PASSWORD, "ab"))


class TestTypedPasswordBoundaries(unittest.TestCase):

    def test_exact_password_logs_in(self):
        store = make_store()
        typed = hash_for_user(store, "sam", PASSWORD)
        self.assertIs(login(store, "sam", typed), store.users["sam"])

    def test_one_character_different_refused(self):
        store = make_store()
        typed = hash_for_user(store, "sam", "pass124")
        with self.assertRaises(ValueError):
            login(store, "sam", typed)

    def test_one_character_longer_refused(self):
        store = make_store()
        typed = hash_for_user(store, "sam", "pass1234")
        with self.assertRaises(ValueError):
            login(store, "sam", typed)

    def test_different_letter_case_refused(self):
        store = make_store()
        typed = hash_for_user(store, "sam", "PASS123")
        with self.assertRaises(ValueError):
            login(store, "sam", typed)


if __name__ == "__main__":
    unittest.main()
