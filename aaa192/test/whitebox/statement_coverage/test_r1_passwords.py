"""R1 password hashing - white-box: statement coverage.

Every statement of hash_password and hash_for_user is run at least once:
  hash_password: raise for a bad password, new salt, raise for an empty
                 salt, raise for a non-hex salt, return
  hash_for_user: return for an unknown user, an empty password, a plain
                 stored password, a bad stored salt, and the hashed result
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.reporting.passwords import hash_for_user, hash_password


class TestPasswordsStatementCoverage(unittest.TestCase):

    def test_hash_password_bad_password(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)

    def test_hash_password_new_salt_and_return(self):
        stored = hash_password(PASSWORD)
        self.assertEqual(stored, expected_hash(PASSWORD, stored[:32]))

    def test_hash_password_empty_salt(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_hash_password_non_hex_salt(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "xyz")

    def test_hash_for_user_every_return(self):
        store = make_store()
        self.assertEqual(hash_for_user(store, "nobody", PASSWORD), PASSWORD)
        self.assertEqual(hash_for_user(store, "sam", ""), "")
        self.assertEqual(hash_for_user(store, "old", PASSWORD), PASSWORD)
        self.assertEqual(hash_for_user(store, "odd", PASSWORD), PASSWORD)
        self.assertEqual(hash_for_user(store, "sam", PASSWORD),
                         expected_hash(PASSWORD))


if __name__ == "__main__":
    unittest.main()
