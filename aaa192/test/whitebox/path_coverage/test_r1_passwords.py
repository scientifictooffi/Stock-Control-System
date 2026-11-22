"""R1 password hashing - white-box: path coverage.

hash_password() feasible paths (D1..D4 as in the branch tests):
  P1 D1                         raise (bad password)
  P2 !D1 D2 !D3 !D4             new salt, return
  P3 !D1 !D2 D3                 raise (empty salt)
  P4 !D1 !D2 !D3 D4             raise (non-hex salt)
  P5 !D1 !D2 !D3 !D4            given salt, return
  (D2 then D3 or D4 is infeasible: a new salt is always a valid hex
  string.) Cyclomatic complexity = 4 decisions + 1 = 5 = paths.
hash_for_user() paths (E1..E4):
  Q1 E1   Q2 !E1 E2   Q3 !E1 !E2 E3   Q4 ... !E3 E4   Q5 ... !E3 !E4
One test per path.
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestHashPasswordPaths(unittest.TestCase):

    def test_p1(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)

    def test_p2(self):
        stored = hash_password(PASSWORD)
        self.assertEqual(len(stored.split("$")[0]), 32)
        self.assertEqual(stored, expected_hash(PASSWORD, stored[:32]))

    def test_p3(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_p4(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "g1")

    def test_p5(self):
        self.assertEqual(hash_password(PASSWORD, SALT),
                         expected_hash(PASSWORD))


class TestHashForUserPaths(unittest.TestCase):

    def test_q1(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)

    def test_q2(self):
        self.assertEqual(hash_for_user(make_store(), "sam", ""), "")

    def test_q3(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_q4(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)

    def test_q5(self):
        self.assertEqual(hash_for_user(make_store(), "sam", PASSWORD),
                         expected_hash(PASSWORD))


if __name__ == "__main__":
    unittest.main()
