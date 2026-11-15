"""R2 check_permission - black-box: random testing.

200 random (username, action) pairs with a fixed seed so the run can be
repeated. Each result is checked against an oracle written from the rules.
"""
import random
import unittest

from member4.test.r2_fixtures import make_store
from stock_control.reporting.auth import ACTIONS, check_permission

SEED = 42
RUNS = 200
USERNAMES = ["david", "alex", "christen", "ghost", "nobody", ""]
EXTRA_ACTIONS = ["fly_to_moon", "", "CHANGE_PRICE", "delete_everything"]
CLERK = {"search_products", "issue_stock", "reserve_stock",
         "process_return", "view_reports"}


def oracle(store, username, action):
    """Return True / False, or ValueError when the call must be refused."""
    user = store.users.get(username)
    if user is None or action not in ACTIONS:
        return ValueError
    if user.role == "admin":
        return True
    if user.role == "manager":
        return action != "manage_users"
    if user.role == "clerk":
        return action in CLERK
    return ValueError


class TestCheckPermissionRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        actions = sorted(ACTIONS) + EXTRA_ACTIONS
        for _ in range(RUNS):
            store = make_store()
            username = rng.choice(USERNAMES)
            action = rng.choice(actions)
            expected = oracle(store, username, action)
            if expected is ValueError:
                with self.assertRaises(ValueError):
                    check_permission(store, username, action)
            else:
                self.assertEqual(expected,
                                 check_permission(store, username, action))


if __name__ == "__main__":
    unittest.main()
