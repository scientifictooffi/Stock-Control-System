"""R2 check_permission - white-box: concolic testing.

Start from one concrete input, record the path it takes, negate the last
decision on that path, solve for a new input and repeat (see
docs/research/R2_check_permission.md for each iteration).
"""
import unittest

from aaa192.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionConcolic(unittest.TestCase):

    def test_iteration_0_seed_clerk_allowed(self):
        self.assertTrue(check_permission(make_store(), "christen",
                                         "issue_stock"))

    def test_iteration_1_negate_d5_action_not_allowed(self):
        self.assertFalse(check_permission(make_store(), "christen",
                                          "change_price"))

    def test_iteration_2_negate_d4_unknown_role(self):
        with self.assertRaisesRegex(ValueError, "unknown role"):
            check_permission(make_store(), "ghost", "issue_stock")

    def test_iteration_3_negate_d3_admin(self):
        self.assertTrue(check_permission(make_store(), "david", "issue_stock"))

    def test_iteration_4_negate_d2_unknown_action(self):
        with self.assertRaisesRegex(ValueError, "unknown action"):
            check_permission(make_store(), "christen", "fly_to_moon")

    def test_iteration_5_negate_d1_unknown_user(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            check_permission(make_store(), "nobody", "issue_stock")


if __name__ == "__main__":
    unittest.main()
