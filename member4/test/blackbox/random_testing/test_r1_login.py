"""R1 login - black-box: random testing.

200 random (username, password) pairs with a fixed seed so the run can be
repeated. Each result is checked against an oracle written from the rules.
"""
import random
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login

SEED = 42
RUNS = 200
USERNAMES = ["sam", "lee", "kim", "nobody", "", "SAM"]
PASSWORDS = ["pass123", "wrong", "", "PASS123", "pass1234"]


def expected_to_fail(store, username, password):
    user = store.users.get(username)
    if user is None or user.locked or not user.active:
        return True
    return user.password != password


class TestLoginRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        for _ in range(RUNS):
            store = make_store()
            username = rng.choice(USERNAMES)
            password = rng.choice(PASSWORDS)
            if expected_to_fail(store, username, password):
                with self.assertRaises(ValueError):
                    login(store, username, password)
            else:
                self.assertIs(login(store, username, password),
                              store.users[username])

    def test_random_sequences_lock_after_3_wrong(self):
        rng = random.Random(SEED)
        for _ in range(RUNS):
            store = make_store()
            wrong = 0
            for _ in range(rng.randint(1, 6)):
                password = rng.choice(["pass123", "wrong"])
                try:
                    login(store, "sam", password)
                    wrong = 0
                except ValueError:
                    wrong += 1
                if wrong >= 3:
                    break
            self.assertEqual(wrong >= 3, store.users["sam"].locked)


if __name__ == "__main__":
    unittest.main()
