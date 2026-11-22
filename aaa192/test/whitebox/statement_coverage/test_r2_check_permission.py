"""R2 check_permission - white-box: statement coverage.

Five tests run every statement in check_permission() at least once
(each raise and each return).
"""
import unittest

from aaa192.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionStatementCoverage(unittest.TestCase):

    def test_statements_unknown_user_and_action_raises(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "nobody", "issue_stock")
        with self.assertRaises(ValueError):
            check_permission(make_store(), "alex", "fly_to_moon")

    def test_statements_admin_return(self):
        self.assertTrue(check_permission(make_store(), "david", "save_data"))

    def test_statements_unknown_role_raise(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "ghost", "issue_stock")

    def test_statements_allowed_return(self):
        self.assertTrue(check_permission(make_store(), "christen",
                                         "issue_stock"))

    def test_statements_denied_return(self):
        self.assertFalse(check_permission(make_store(), "christen",
                                          "change_price"))


if __name__ == "__main__":
    unittest.main()
