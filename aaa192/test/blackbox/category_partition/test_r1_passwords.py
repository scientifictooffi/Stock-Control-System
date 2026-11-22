"""R1 password hashing - black-box: category partition (Lab 8).

Specification: r1_passwords.tsl (parameters Password, Salt, User at
login, Typed password, with their choices and [error] / [single] /
[property] / [if] constraints). Test frames: r1_passwords.frames.txt,
generated with TSLgenerator. One test per frame (14 frames).
"""
import unittest

from aaa192.test.r1_passwords_fixtures import (
    PASSWORD, SALT, expected_hash, make_store)
from stock_control.models import User
from stock_control.reporting.auth import login
from stock_control.reporting.passwords import hash_for_user, hash_password
from stock_control.store import Store


def store_with(stored_password):
    store = Store()
    store.users["sam"] = User("sam", stored_password, "admin")
    return store


def typed_matches(store, typed):
    """True when login() accepts the typed password after hashing."""
    try:
        login(store, "sam", hash_for_user(store, "sam", typed))
        return True
    except ValueError:
        return False


class TestPasswordsCategoryPartition(unittest.TestCase):

    def test_frame_01_password_empty_error(self):
        with self.assertRaises(ValueError):
            hash_password("", SALT)

    def test_frame_02_password_not_string_error(self):
        with self.assertRaises(ValueError):
            hash_password(["pass"], SALT)

    def test_frame_03_password_one_character(self):
        self.assertEqual(hash_password("x", SALT), expected_hash("x"))

    def test_frame_04_salt_empty_error(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "")

    def test_frame_05_salt_not_hex_error(self):
        with self.assertRaises(ValueError):
            hash_password(PASSWORD, "xyz")

    def test_frame_06_unknown_user(self):
        self.assertEqual(hash_for_user(make_store(), "nobody", PASSWORD),
                         PASSWORD)

    def test_frame_07_user_stored_in_plain_text(self):
        self.assertEqual(hash_for_user(make_store(), "old", PASSWORD),
                         PASSWORD)

    def test_frame_08_stored_value_not_salt_and_hash(self):
        self.assertEqual(hash_for_user(make_store(), "odd", PASSWORD),
                         PASSWORD)

    def test_frame_09_typed_password_different_case(self):
        store = store_with(hash_password(PASSWORD, SALT))
        self.assertFalse(typed_matches(store, PASSWORD.upper()))

    def test_frame_10_typed_password_empty_error(self):
        store = store_with(hash_password(PASSWORD, SALT))
        self.assertEqual(hash_for_user(store, "sam", ""), "")
        self.assertFalse(typed_matches(store, ""))

    def test_frame_11_no_salt_hashed_user_same_password(self):
        store = store_with(hash_password(PASSWORD))
        self.assertTrue(typed_matches(store, PASSWORD))

    def test_frame_12_no_salt_hashed_user_one_char_different(self):
        store = store_with(hash_password(PASSWORD))
        self.assertFalse(typed_matches(store, "pass124"))

    def test_frame_13_hex_salt_hashed_user_same_password(self):
        store = store_with(hash_password(PASSWORD, SALT))
        self.assertTrue(typed_matches(store, PASSWORD))

    def test_frame_14_hex_salt_hashed_user_one_char_different(self):
        store = store_with(hash_password(PASSWORD, SALT))
        self.assertFalse(typed_matches(store, "pass124"))


if __name__ == "__main__":
    unittest.main()
