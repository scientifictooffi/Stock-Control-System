import unittest
from ab1409.test.s1_fixtures import (
    ACTIVE_ID, ACTIVE_NAME, EMAIL, NEW_NAME, PHONE, SUSPENDED_ID,
    SUSPENDED_NAME, UNKNOWN_ID, make_store, snapshot)
from stock_control.purchasing.suppliers import save_supplier


class TestSaveSupplierPathCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_path_refused(self, error, message, *args, **kwargs):
        with self.assertRaises(error) as ctx:
            save_supplier(self.store, *args, **kwargs)
        self.assertIn(message, str(ctx.exception))
        self.assertEqual(self.store, self.before)

    def test_path_1_unknown_supplier_id(self):
        self.assert_path_refused(
            KeyError, "does not exist", NEW_NAME, EMAIL, PHONE,
            supplier_id=UNKNOWN_ID)

    def test_path_2_name_missing(self):
        self.assert_path_refused(
            ValueError, "name is required", "", EMAIL, PHONE)

    def test_path_3_name_in_use(self):
        self.assert_path_refused(
            ValueError, "already used", ACTIVE_NAME, EMAIL, PHONE)

    def test_path_4_bad_email(self):
        self.assert_path_refused(
            ValueError, "email", NEW_NAME, "x@y", PHONE)

    def test_path_4_email_not_text(self):
        self.assert_path_refused(
            ValueError, "email", NEW_NAME, 42, PHONE)

    def test_path_5_phone_not_text(self):
        self.assert_path_refused(
            ValueError, "phone", NEW_NAME, EMAIL, 42)

    def test_path_5_bad_phone(self):
        self.assert_path_refused(
            ValueError, "phone", NEW_NAME, EMAIL, "abc")

    def test_path_6_bad_status(self):
        self.assert_path_refused(
            ValueError, "status", NEW_NAME, EMAIL, PHONE, "retired")

    def test_path_7_create_new_supplier(self):
        supplier = save_supplier(self.store, NEW_NAME, EMAIL, PHONE)
        self.assertEqual(supplier.supplier_id, "SUP0003")
        self.assertEqual(len(self.store.suppliers), 3)
        self.assertEqual(self.store.suppliers["SUP0003"].status, "active")

    def test_path_8_update_active_supplier(self):
        supplier = save_supplier(
            self.store, ACTIVE_NAME, EMAIL, PHONE, "suspended", ACTIVE_ID)
        self.assertIs(supplier, self.store.suppliers[ACTIVE_ID])
        self.assertEqual(supplier.status, "suspended")
        self.assertEqual(len(self.store.suppliers), 2)

    def test_path_9_suspended_not_reactivated(self):
        self.assert_path_refused(
            ValueError, "only be reactivated", SUSPENDED_NAME,
            "hello@delta.co.uk", "0116 496 0002", "suspended", SUSPENDED_ID)

    def test_path_10_suspended_details_changed(self):
        self.assert_path_refused(
            ValueError, "details cannot be changed", SUSPENDED_NAME,
            "new@delta.co.uk", "0116 496 0002", "active", SUSPENDED_ID)

    def test_path_11_suspended_reactivated(self):
        supplier = save_supplier(
            self.store, SUSPENDED_NAME, "hello@delta.co.uk", "0116 496 0002",
            "active", SUSPENDED_ID)
        self.assertEqual(supplier.status, "active")
        self.assertEqual(len(self.store.suppliers), 2)


if __name__ == "__main__":
    unittest.main()
