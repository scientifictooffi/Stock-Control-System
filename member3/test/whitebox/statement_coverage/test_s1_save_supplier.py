import unittest
from member3.test.s1_fixtures import (
    ACTIVE_ID, ACTIVE_NAME, EMAIL, NEW_NAME, PHONE, SUSPENDED_ID,
    SUSPENDED_NAME, UNKNOWN_ID, make_store)
from stock_control.purchasing.suppliers import save_supplier


class TestSaveSupplierStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_statement_raise_unknown_supplier_id(self):
        with self.assertRaises(KeyError):
            save_supplier(
                self.store, NEW_NAME, EMAIL, PHONE, supplier_id=UNKNOWN_ID)

    def test_statement_raise_name_required(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, " ", EMAIL, PHONE)

    def test_statement_raise_name_in_use(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, ACTIVE_NAME, EMAIL, PHONE)

    def test_statement_raise_email(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, "nope", PHONE)

    def test_statement_raise_email_not_text(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, 99, PHONE)

    def test_statement_raise_phone_not_text(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, 99)

    def test_statement_raise_phone_characters(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, "0116-ABC-4960")

    def test_statement_raise_phone(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, "12")

    def test_statement_raise_status(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, NEW_NAME, EMAIL, PHONE, "gone")

    def test_statement_raise_suspended_not_reactivated(self):
        with self.assertRaises(ValueError):
            save_supplier(
                self.store, SUSPENDED_NAME, "hello@delta.co.uk",
                "0116 496 0002", "suspended", SUSPENDED_ID)

    def test_statement_raise_suspended_details_changed(self):
        with self.assertRaises(ValueError):
            save_supplier(
                self.store, SUSPENDED_NAME, "new@delta.co.uk",
                "0116 496 0002", "active", SUSPENDED_ID)

    def test_statements_create_new_supplier(self):
        supplier = save_supplier(self.store, NEW_NAME, EMAIL, PHONE)
        self.assertEqual(supplier.supplier_id, "SUP0003")
        self.assertEqual(self.store.suppliers["SUP0003"].email, EMAIL)

    def test_statements_update_active_supplier(self):
        supplier = save_supplier(
            self.store, "Acme Pipes Ltd", EMAIL, PHONE, "suspended",
            ACTIVE_ID)
        self.assertEqual(supplier.name, "Acme Pipes Ltd")
        self.assertEqual(self.store.suppliers[ACTIVE_ID].status, "suspended")

    def test_statements_reactivate_suspended_supplier(self):
        supplier = save_supplier(
            self.store, SUSPENDED_NAME, "hello@delta.co.uk", "0116 496 0002",
            "active", SUSPENDED_ID)
        self.assertEqual(supplier.status, "active")


if __name__ == "__main__":
    unittest.main()
