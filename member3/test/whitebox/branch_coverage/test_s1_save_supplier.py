import unittest
from member3.test.s1_fixtures import (
    ACTIVE_ID, ACTIVE_NAME, EMAIL, NEW_NAME, PHONE, SUSPENDED_ID,
    SUSPENDED_NAME, UNKNOWN_ID, make_store, snapshot)
from stock_control.purchasing.suppliers import save_supplier


class TestSaveSupplierBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_branch_supplier_id_none_false(self):
        self.assertEqual(
            save_supplier(self.store, NEW_NAME, EMAIL, PHONE).supplier_id,
            "SUP0003")

    def test_branch_supplier_id_given_and_unknown_true(self):
        with self.assertRaises(KeyError):
            save_supplier(
                self.store, NEW_NAME, EMAIL, PHONE, supplier_id=UNKNOWN_ID)

    def test_branch_supplier_id_given_and_known_false(self):
        save_supplier(
            self.store, ACTIVE_NAME, EMAIL, PHONE, supplier_id=ACTIVE_ID)
        self.assertEqual(self.store.suppliers[ACTIVE_ID].email, EMAIL)

    def test_branch_name_not_text_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, 123, EMAIL, PHONE)

    def test_branch_name_blank_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, "", EMAIL, PHONE)

    def test_branch_name_in_use_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, ACTIVE_NAME.upper(), EMAIL, PHONE)

    def test_branch_name_in_use_by_itself_false(self):
        save_supplier(
            self.store, ACTIVE_NAME, EMAIL, PHONE, supplier_id=ACTIVE_ID)
        self.assertEqual(len(self.store.suppliers), 2)

    def test_branch_email_not_text_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, None, PHONE)

    def test_branch_email_pattern_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, "a@b", PHONE)

    def test_branch_phone_not_text_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, None)

    def test_branch_phone_pattern_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, "0116-ABC-1234")

    def test_branch_phone_too_few_digits_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, "123456")

    def test_branch_phone_too_many_digits_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, "1234567890123456")

    def test_branch_status_not_allowed_true(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, PHONE, "paused")

    def test_branch_existing_is_none_true(self):
        save_supplier(self.store, NEW_NAME, EMAIL, PHONE)
        self.assertIn("SUP0003", self.store.suppliers)

    def test_branch_existing_suspended_false(self):
        save_supplier(
            self.store, ACTIVE_NAME, EMAIL, PHONE, "active", ACTIVE_ID)
        self.assertEqual(self.store.suppliers[ACTIVE_ID].status, "active")

    def test_branch_suspended_status_not_active_true(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            save_supplier(
                self.store, SUSPENDED_NAME, "hello@delta.co.uk",
                "0116 496 0002", "suspended", SUSPENDED_ID)
        self.assertEqual(self.store, before)

    def test_branch_suspended_name_changed_true(self):
        with self.assertRaises(ValueError):
            save_supplier(
                self.store, "Delta Tools 2", "hello@delta.co.uk",
                "0116 496 0002", "active", SUSPENDED_ID)

    def test_branch_suspended_phone_changed_true(self):
        with self.assertRaises(ValueError):
            save_supplier(
                self.store, SUSPENDED_NAME, "hello@delta.co.uk",
                "0116 496 0003", "active", SUSPENDED_ID)

    def test_branch_suspended_nothing_changed_false(self):
        supplier = save_supplier(
            self.store, SUSPENDED_NAME, " hello@delta.co.uk ",
            "0116 496 0002 ", "active", SUSPENDED_ID)
        self.assertEqual(supplier.status, "active")


if __name__ == "__main__":
    unittest.main()
