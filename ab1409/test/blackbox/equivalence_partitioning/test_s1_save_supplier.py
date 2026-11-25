import unittest
from ab1409.test.s1_fixtures import (
    ACTIVE_ID, ACTIVE_NAME, EMAIL, NEW_NAME, PHONE, SUSPENDED_ID,
    SUSPENDED_NAME, UNKNOWN_ID, make_store, snapshot)
from stock_control.purchasing.suppliers import save_supplier


class TestSaveSupplierValidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_valid_class_new_active_supplier(self):
        supplier = save_supplier(self.store, NEW_NAME, EMAIL, PHONE)
        self.assertEqual(supplier.supplier_id, "SUP0003")
        self.assertEqual(supplier.status, "active")
        self.assertIs(self.store.suppliers["SUP0003"], supplier)

    def test_valid_class_new_suspended_supplier(self):
        supplier = save_supplier(
            self.store, NEW_NAME, EMAIL, PHONE, "suspended")
        self.assertEqual(supplier.status, "suspended")

    def test_valid_class_details_are_trimmed(self):
        supplier = save_supplier(
            self.store, "  Midlands Pipe Co ", " " + EMAIL + " ", " " + PHONE)
        self.assertEqual(
            (supplier.name, supplier.email, supplier.phone),
            (NEW_NAME, EMAIL, PHONE))

    def test_valid_class_edit_active_supplier_keeps_own_name(self):
        supplier = save_supplier(
            self.store, ACTIVE_NAME, "new@acme.co.uk", "0116 496 0099",
            supplier_id=ACTIVE_ID)
        self.assertEqual(supplier.email, "new@acme.co.uk")
        self.assertEqual(supplier.min_order_value, 50.0)
        self.assertEqual(supplier.deliveries_total, 5)
        self.assertEqual(len(self.store.suppliers), 2)

    def test_valid_class_suspend_active_supplier(self):
        supplier = save_supplier(
            self.store, ACTIVE_NAME, "orders@acme.co.uk", "0116 496 0001",
            "suspended", ACTIVE_ID)
        self.assertEqual(supplier.status, "suspended")

    def test_valid_class_reactivate_suspended_supplier(self):
        supplier = save_supplier(
            self.store, SUSPENDED_NAME, "hello@delta.co.uk", "0116 496 0002",
            "active", SUSPENDED_ID)
        self.assertEqual(supplier.status, "active")


class TestSaveSupplierInvalidClasses(unittest.TestCase):

    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args, **kwargs):
        with self.assertRaises(error):
            save_supplier(self.store, *args, **kwargs)
        self.assertEqual(self.store, self.before)

    def test_name_empty(self):
        self.assert_refused(ValueError, "", EMAIL, PHONE)

    def test_name_only_spaces(self):
        self.assert_refused(ValueError, "   ", EMAIL, PHONE)

    def test_name_not_text(self):
        self.assert_refused(ValueError, None, EMAIL, PHONE)

    def test_name_already_used(self):
        self.assert_refused(ValueError, ACTIVE_NAME, EMAIL, PHONE)

    def test_name_already_used_other_letter_case(self):
        self.assert_refused(ValueError, "  acme plumbing LTD ", EMAIL, PHONE)

    def test_name_used_by_another_supplier_when_editing(self):
        self.assert_refused(
            ValueError, SUSPENDED_NAME, EMAIL, PHONE, supplier_id=ACTIVE_ID)

    def test_email_without_at_sign(self):
        self.assert_refused(ValueError, NEW_NAME, "sales.midlandspipe.co.uk",
                            PHONE)

    def test_email_without_domain_dot(self):
        self.assert_refused(ValueError, NEW_NAME, "sales@midlandspipe", PHONE)

    def test_email_with_space(self):
        self.assert_refused(ValueError, NEW_NAME, "sa les@pipe.co.uk", PHONE)

    def test_email_not_text(self):
        self.assert_refused(ValueError, NEW_NAME, 12345, PHONE)

    def test_phone_with_letters(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, "0116-CALL-NOW")

    def test_phone_too_short(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, "12345")

    def test_phone_plus_in_the_middle(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, "0116+4960000")

    def test_phone_not_text(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, 1164960000)

    def test_status_unknown_word(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, PHONE, "closed")

    def test_status_wrong_letter_case(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, PHONE, "Active")

    def test_status_missing(self):
        self.assert_refused(ValueError, NEW_NAME, EMAIL, PHONE, None)

    def test_unknown_supplier_id(self):
        self.assert_refused(
            KeyError, NEW_NAME, EMAIL, PHONE, supplier_id=UNKNOWN_ID)

    def test_suspended_supplier_cannot_stay_suspended(self):
        self.assert_refused(
            ValueError, SUSPENDED_NAME, "hello@delta.co.uk", "0116 496 0002",
            "suspended", SUSPENDED_ID)

    def test_suspended_supplier_cannot_change_email(self):
        self.assert_refused(
            ValueError, SUSPENDED_NAME, "other@delta.co.uk", "0116 496 0002",
            "active", SUSPENDED_ID)

    def test_suspended_supplier_cannot_change_name(self):
        self.assert_refused(
            ValueError, "Delta Tools Ltd", "hello@delta.co.uk",
            "0116 496 0002", "active", SUSPENDED_ID)


if __name__ == "__main__":
    unittest.main()
