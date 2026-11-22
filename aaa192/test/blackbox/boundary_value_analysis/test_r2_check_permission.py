"""R2 check_permission - black-box: boundary value analysis.

The boundaries are the edges of each role's permission set and of the
list of known actions: the action just inside a role's set, the one
just outside it, and strings that are almost a known action
(empty, wrong case, extra space).
"""
import unittest

from aaa192.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionBoundaryValues(unittest.TestCase):

    def test_manager_last_allowed_action(self):
        self.assertTrue(check_permission(make_store(), "alex", "save_data"))

    def test_manager_first_action_outside_set(self):
        self.assertFalse(check_permission(make_store(), "alex",
                                          "manage_users"))

    def test_clerk_inside_edge_view_reports(self):
        self.assertTrue(check_permission(make_store(), "christen",
                                         "view_reports"))

    def test_clerk_outside_edge_view_audit_log(self):
        self.assertFalse(check_permission(make_store(), "christen",
                                          "view_audit_log"))

    def test_empty_action_refused(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "david", "")

    def test_wrong_case_action_refused(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "david", "Issue_Stock")

    def test_action_with_space_refused(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "david", "issue_stock ")

    def test_empty_username_refused(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "", "issue_stock")


if __name__ == "__main__":
    unittest.main()
