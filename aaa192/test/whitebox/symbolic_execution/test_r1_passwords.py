"""R1 password hashing - white-box: symbolic execution.

One test per leaf of the symbolic execution trees in
docs/research/R1_passwords.md, using the solution of that leaf's path
condition (PC).
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestHashPasswordSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_password_empty(self):
        with self.assertRaisesRegex(ValueError, "password"):
            hash_password("", SALT)

    def test_leaf_l2_pc_salt_none(self):
        stored = hash_password(PASSWORD, None)
        self.assertEqual(stored, expected_hash(PASSWORD, stored[:32]))

    def test_leaf_l3_pc_salt_empty(self):
        with self.assertRaisesRegex(ValueError, "salt"):
            hash_password(PASSWORD, "")

    def test_leaf_l4_pc_salt_not_hex(self):
        with self.assertRaisesRegex(ValueError, "salt"):
            hash_password(PASSWORD, "xyz")

    def test_leaf_l5_pc_salt_hex(self):
        self.assertEqual(hash_password(PASSWORD, SALT),
                         expected_hash(PASSWORD))


class TestHashForUserSymbolicExecution(unittest.TestCase):

    def test_leaf_m1_pc_user_missing(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)

    def test_leaf_m2_pc_password_empty(self):
        self.assertEqual(hash_for_user(make_store(), "sam", ""), "")

    def test_leaf_m3_pc_no_separator(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_leaf_m4_pc_salt_not_hex(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)

    def test_leaf_m5_pc_salt_hex(self):
        self.assertEqual(hash_for_user(make_store(), "sam", PASSWORD),
                         expected_hash(PASSWORD))


if __name__ == "__main__":
    unittest.main()
