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


class TestSaveSupplierSymbolicExecution(unittest.TestCase):

    def test_leaf_l1_pc_id_given_and_unknown(self):
        with self.assertRaises(KeyError):
            save_supplier(make_store(), "Zed", "z@zed.co", "01164960003",
                          "active", "SUP0009")

    def test_leaf_l2_pc_name_blank(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "  ", "z@zed.co", "01164960003")

    def test_leaf_l3_pc_name_used_by_other(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "ACME", "z@zed.co", "01164960003")

    def test_leaf_l4_pc_email_invalid(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "zed.co", "01164960003")

    def test_leaf_l4_pc_email_not_text(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", 5, "01164960003")

    def test_leaf_l5_pc_phone_not_text(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "z@zed.co", 5)

    def test_leaf_l5_pc_phone_bad_characters(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "z@zed.co", "0116-CALL-NOW")

    def test_leaf_l5_pc_phone_invalid(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "z@zed.co", "999")

    def test_leaf_l6_pc_status_invalid(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Zed", "z@zed.co", "01164960003",
                          "dormant")

    def test_leaf_l7_pc_new_supplier(self):
        store = make_store()
        supplier = save_supplier(store, "Zed", "z@zed.co", "01164960003")
        self.assertEqual("SUP0003", supplier.supplier_id)
        self.assertEqual(3, len(store.suppliers))

    def test_leaf_l8_pc_existing_active(self):
        store = make_store()
        save_supplier(store, "Acme", "new@acme.co", "01164960001", "active",
                      "SUP0001")
        self.assertEqual("new@acme.co", store.suppliers["SUP0001"].email)

    def test_leaf_l9_pc_suspended_status_not_active(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Delta", "d@delta.co", "01164960002",
                          "suspended", "SUP0002")

    def test_leaf_l10_pc_suspended_details_differ(self):
        with self.assertRaises(ValueError):
            save_supplier(make_store(), "Delta", "x@delta.co", "01164960002",
                          "active", "SUP0002")

    def test_leaf_l11_pc_suspended_reactivated(self):
        store = make_store()
        save_supplier(store, "Delta", "d@delta.co", "01164960002", "active",
                      "SUP0002")
        self.assertEqual("active", store.suppliers["SUP0002"].status)


if __name__ == "__main__":
    unittest.main()
