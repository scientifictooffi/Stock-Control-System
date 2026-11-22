"""R2 check_permission - black-box: equivalence partitioning.

Input classes taken from the four rules:
  username: exists (valid) | does not exist (invalid)
  role:     admin | manager | clerk (valid) | unknown role (invalid)
  action:   known (valid) | unknown (invalid)
  result:   allowed for the role | not allowed for the role
One test per class.
"""
import unittest

from aaa192.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionEquivalencePartitioning(unittest.TestCase):

    def test_admin_known_action_allowed(self):
        self.assertTrue(check_permission(make_store(), "david",
                                         "manage_users"))

    def test_manager_allowed_action(self):
        self.assertTrue(check_permission(make_store(), "alex", "change_price"))

    def test_manager_not_allowed_action(self):
        self.assertFalse(check_permission(make_store(), "alex",
                                          "manage_users"))

    def test_clerk_allowed_action(self):
        self.assertTrue(check_permission(make_store(), "christen",
                                         "issue_stock"))

    def test_clerk_cannot_change_prices(self):
        self.assertFalse(check_permission(make_store(), "christen",
                                          "change_price"))

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "nobody", "issue_stock")

    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "alex", "fly_to_moon")

    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "ghost", "issue_stock")


if __name__ == "__main__":
    unittest.main()
