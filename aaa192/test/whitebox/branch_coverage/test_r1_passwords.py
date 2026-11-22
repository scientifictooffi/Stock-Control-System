"""R1 password hashing - white-box: branch coverage.

Decisions in hash_password():
  D1 password not a string or empty     D2 salt is None
  D3 salt not a string or empty         D4 bytes.fromhex(salt) fails
Decisions in hash_for_user():
  E1 user is None                       E2 password not a string or empty
  E3 no "$" in the stored password      E4 hash_password raises ValueError
Each decision is made True once and False once.
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestHashPasswordBranchCoverage(unittest.TestCase):

    def test_d1_true(self):
        with self.assertRaises(ValueError):
            hash_password(None, SALT)

    def test_d1_false_d2_true(self):
        stored = hash_password(PASSWORD)
        self.assertEqual(stored, expected_hash(PASSWORD, stored[:32]))

    def test_d2_false_d3_true(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_d3_false_d4_true(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "not-hex")

    def test_d3_false_d4_false(self):
        self.assertEqual(hash_password(PASSWORD, SALT),
                         expected_hash(PASSWORD))


class TestHashForUserBranchCoverage(unittest.TestCase):

    def test_e1_true(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)

    def test_e1_false_e2_true(self):
        self.assertEqual(hash_for_user(make_store(), "sam", ""), "")

    def test_e2_false_e3_true(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_e3_false_e4_true(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)

    def test_e3_false_e4_false(self):
        self.assertEqual(hash_for_user(make_store(), "sam", PASSWORD),
                         expected_hash(PASSWORD))


if __name__ == "__main__":
    unittest.main()
