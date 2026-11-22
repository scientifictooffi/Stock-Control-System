"""R2 check_permission - white-box: branch coverage.

Decisions in check_permission():
  D1 user is None            D2 action not in ACTIONS
  D3 role == "admin"         D4 role not in ROLE_PERMISSIONS
  D5 action in the role's permissions
Each decision is made True once and False once.
"""
import unittest

from aaa192.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionBranchCoverage(unittest.TestCase):

    def test_d1_true(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "nobody", "issue_stock")

    def test_d1_false_d2_true(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "david", "fly_to_moon")

    def test_d2_false_d3_true(self):
        self.assertTrue(check_permission(make_store(), "david",
                                         "manage_users"))

    def test_d3_false_d4_true(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "ghost", "issue_stock")

    def test_d4_false_d5_true(self):
        self.assertTrue(check_permission(make_store(), "alex", "change_price"))

    def test_d5_false(self):
        self.assertFalse(check_permission(make_store(), "alex",
                                          "manage_users"))


if __name__ == "__main__":
    unittest.main()
