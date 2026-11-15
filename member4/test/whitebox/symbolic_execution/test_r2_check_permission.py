"""R2 check_permission - white-box: symbolic execution.

One test per leaf of the symbolic execution tree in
docs/research/R2_check_permission.md, using the solution of that leaf's
path condition (PC).
"""
import unittest

from member4.test.r2_fixtures import make_store
from stock_control.reporting.auth import check_permission


class TestCheckPermissionSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_user_missing(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "nobody", "issue_stock")

    def test_leaf_l2_pc_action_unknown(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "christen", "fly_to_moon")

    def test_leaf_l3_pc_role_admin(self):
        self.assertTrue(check_permission(make_store(), "david", "save_data"))

    def test_leaf_l4_pc_role_unknown(self):
        with self.assertRaises(ValueError):
            check_permission(make_store(), "ghost", "view_reports")

    def test_leaf_l5_pc_action_in_role_set(self):
        self.assertTrue(check_permission(make_store(), "alex", "stocktake"))

    def test_leaf_l6_pc_action_not_in_role_set(self):
        self.assertFalse(check_permission(make_store(), "christen",
                                          "approve_order"))


if __name__ == "__main__":
    unittest.main()
