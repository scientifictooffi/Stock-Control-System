"""R1 password hashing - black-box: random testing.

50 random passwords and salts, and 50 random login attempts, with a
fixed seed so the run can be repeated. Each result is checked against
an oracle written from the rules: the result equals PBKDF2 of the
password with the salt, the same password and salt give the same
result, the stored hash is never the plain password, and only the right
password matches after hash_for_user.
"""
import random
import string
import unittest

from aaa192.test.r1_passwords_fixtures import expected_hash
from stock_control.models import User
from stock_control.reporting.passwords import hash_for_user, hash_password
from stock_control.store import Store

SEED = 7
RUNS = 50
CHARS = string.ascii_letters + string.digits + string.punctuation


def random_password(rng):
    return "".join(rng.choices(CHARS, k=rng.randint(1, 20)))


class TestPasswordsRandom(unittest.TestCase):

    def test_random_passwords_and_salts(self):
        rng = random.Random(SEED)
        for _ in range(RUNS):
            password = random_password(rng)
            salt = "".join(rng.choices("0123456789abcdef", k=32))
            with self.subTest(password=password, salt=salt):
                stored = hash_password(password, salt)
                self.assertEqual(stored, expected_hash(password, salt))
                self.assertEqual(stored, hash_password(password, salt))
                self.assertNotEqual(stored.split("$")[1], password)

    def test_random_typed_passwords(self):
        rng = random.Random(SEED)
        for _ in range(RUNS):
            real = random_password(rng)
            typed = rng.choice([real, random_password(rng)])
            store = Store()
            store.users["u"] = User("u", hash_password(real), "clerk")
            with self.subTest(real=real, typed=typed):
                matches = (hash_for_user(store, "u", typed)
                           == store.users["u"].password)
                self.assertEqual(matches, typed == real)


if __name__ == "__main__":
    unittest.main()
