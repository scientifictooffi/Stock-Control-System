"""R1 password hashing - white-box: concolic testing.

Start from one concrete input, record the path it takes, negate the last
decision on that path, solve for a new input and repeat (see
docs/research/R1_passwords.md for each iteration).
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestHashPasswordConcolic(unittest.TestCase):

    def test_iteration_0_seed_hex_salt(self):
        self.assertEqual(hash_password(PASSWORD, SALT),
                         expected_hash(PASSWORD))

    def test_iteration_1_negate_d4_salt_not_hex(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "xyz")

    def test_iteration_2_negate_d3_salt_empty(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_iteration_3_negate_d2_salt_none(self):
        stored = hash_password(PASSWORD, None)
        self.assertEqual(stored, expected_hash(PASSWORD, stored[:32]))

    def test_iteration_4_negate_d1_password_empty(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)


class TestHashForUserConcolic(unittest.TestCase):

    def test_iteration_0_seed_hashed_user(self):
        self.assertEqual(hash_for_user(make_store(), "sam", PASSWORD),
                         expected_hash(PASSWORD))

    def test_iteration_1_negate_e4_salt_not_hex(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)

    def test_iteration_2_negate_e3_no_separator(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_iteration_3_negate_e2_password_empty(self):
        self.assertEqual(hash_for_user(make_store(), "sam", ""), "")

    def test_iteration_4_negate_e1_unknown_user(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)


if __name__ == "__main__":
    unittest.main()
