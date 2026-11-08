"""R1 login - white-box: path coverage.

login() has 6 independent paths (cyclomatic complexity = 5 decisions + 1 = 6):
  P1 D1=T                       -> "does not exist"
  P2 D1=F D2=T                  -> "account is locked"
  P3 D1=F D2=F D3=T             -> "account is inactive"
  P4 D1..D3=F D4=T D5=T         -> "now locked"
  P5 D1..D3=F D4=T D5=F         -> "wrong password"
  P6 D1..D3=F D4=F              -> returns User
"""
import unittest

from member4.test.r1_fixtures import make_store
from stock_control.reporting.auth import login


class TestLoginPathCoverage(unittest.TestCase):

    def test_path_1_unknown_user(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            login(make_store(), "nobody", "pass123")

    def test_path_2_locked(self):
        with self.assertRaisesRegex(ValueError, "account is locked"):
            login(make_store(), "kim", "pass123")

    def test_path_3_inactive(self):
        with self.assertRaisesRegex(ValueError, "inactive"):
            login(make_store(), "lee", "pass123")

    def test_path_4_wrong_password_locks(self):
        store = make_store()
        store.users["sam"].failed_logins = 2
        with self.assertRaisesRegex(ValueError, "now locked"):
            login(store, "sam", "wrong")

    def test_path_5_wrong_password_not_yet_locked(self):
        with self.assertRaisesRegex(ValueError, "^wrong password$"):
            login(make_store(), "sam", "wrong")

    def test_path_6_success(self):
        store = make_store()
        self.assertEqual("sam", login(store, "sam", "pass123").username)


if __name__ == "__main__":
    unittest.main()
