import unittest
from stock_control.models import Supplier
from stock_control.purchasing.suppliers import save_supplier
from stock_control.store import Store


def make_store():
    store = Store()
    store.suppliers["SUP0001"] = Supplier(
        "SUP0001", "Acme", "a@acme.co", "01164960001")
    store.suppliers["SUP0002"] = Supplier(
        "SUP0002", "Delta", "d@delta.co", "01164960002", "suspended")
    return store


class TestSaveSupplierConcolic(unittest.TestCase):

    def test_iteration_0_seed_input_reactivate(self):
        store = make_store()
        supplier = save_supplier(store, "Delta", "d@delta.co", "01164960002",
                                 "active", "SUP0002")
        self.assertEqual("active", supplier.status)

    def test_iteration_1_negate_d10_details_unchanged(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Delta", "other@delta.co",
                          "01164960002", "active", "SUP0002")

    def test_iteration_2_negate_d9_status_is_active(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Delta", "d@delta.co", "01164960002",
                          "suspended", "SUP0002")

    def test_iteration_3_negate_d8_existing_not_suspended(self):
        store = make_store()
        save_supplier(store, "Acme", "a@acme.co", "01164960001", "suspended",
                      "SUP0001")
        self.assertEqual("suspended", store.suppliers["SUP0001"].status)

    def test_iteration_4_negate_d7_no_existing_supplier(self):
        store = make_store()
        supplier = save_supplier(store, "Zed", "z@zed.co", "01164960003")
        self.assertEqual("SUP0003", supplier.supplier_id)

    def test_iteration_5_negate_d6_status_not_allowed(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "z@zed.co", "01164960003",
                          "retired")

    def test_iteration_6_negate_d5_phone_not_valid(self):
        for phone in ("12", "0116-CALL-NOW", 12345678):
            with self.subTest(phone=phone):
                with self.assertRaises(ValueError):
                    save_supplier(make_store(), "Zed", "z@zed.co", phone)

    def test_iteration_7_negate_d4_email_not_valid(self):
        for email in ("zed", 5):
            with self.subTest(email=email):
                with self.assertRaises(ValueError):
                    save_supplier(make_store(), "Zed", email, "01164960003")

    def test_iteration_8_negate_d3_name_not_unique(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "acme", "z@zed.co", "01164960003")

    def test_iteration_9_negate_d2_name_not_text(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), None, "z@zed.co", "01164960003")

    def test_iteration_10_negate_d1_unknown_supplier_id(self):
        with self.assertRaises(KeyError):
            save_supplier(make_store(), "Zed", "z@zed.co", "01164960003",
                          "active", "SUP0042")


if __name__ == "__main__":
    unittest.main()
