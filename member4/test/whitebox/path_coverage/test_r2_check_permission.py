"""R2 check_permission - white-box: path coverage.

check_permission() has 6 independent paths
(cyclomatic complexity = 5 decisions + 1 = 6):
  P1 D1=T                         -> "does not exist"
  P2 D1=F D2=T                    -> "unknown action"
  P3 D1=F D2=F D3=T               -> True (admin)
  P4 D1=F D2=F D3=F D4=T          -> "unknown role"
  P5 D1..D4=F D5=T                -> True (allowed)
  P6 D1..D4=F D5=F                -> False (not allowed)
"""
import unittest

from member4.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionPathCoverage(unittest.TestCase):

    def test_path_1_unknown_user(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            check_permission(make_store(), "nobody", "issue_stock")

    def test_path_2_unknown_action(self):
        with self.assertRaisesRegex(ValueError, "unknown action"):
            check_permission(make_store(), "alex", "fly_to_moon")

    def test_path_3_admin(self):
        self.assertIs(True, check_permission(make_store(), "david",
                                             "manage_users"))

    def test_path_4_unknown_role(self):
        with self.assertRaisesRegex(ValueError, "unknown role"):
            check_permission(make_store(), "ghost", "issue_stock")

    def test_path_5_allowed(self):
        self.assertIs(True, check_permission(make_store(), "christen",
                                             "process_return"))

    def test_path_6_not_allowed(self):
        self.assertIs(False, check_permission(make_store(), "christen",
                                              "change_price"))


if __name__ == "__main__":
    unittest.main()
