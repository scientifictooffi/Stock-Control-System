import unittest
from ab1409.test.s1_fixtures import (
    ACTIVE_NAME, EMAIL, NEW_NAME, make_store, snapshot)
from stock_control.purchasing.suppliers import save_supplier


class TestNameBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def test_name_empty_is_rejected(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, "", EMAIL, "01164960000")

    def test_name_one_character_is_accepted(self):
        supplier = save_supplier(self.store, "A", EMAIL, "01164960000")
        self.assertEqual(supplier.name, "A")

    def test_name_one_character_plus_spaces_is_accepted(self):
        supplier = save_supplier(self.store, "  A  ", EMAIL, "01164960000")
        self.assertEqual(supplier.name, "A")

    def test_name_one_letter_different_is_accepted(self):
        supplier = save_supplier(
            self.store, ACTIVE_NAME + "s", EMAIL, "01164960000")
        self.assertEqual(supplier.name, ACTIVE_NAME + "s")

    def test_name_one_letter_shorter_is_accepted(self):
        supplier = save_supplier(
            self.store, ACTIVE_NAME[:-1], EMAIL, "01164960000")
        self.assertEqual(supplier.name, ACTIVE_NAME[:-1])

    def test_name_identical_is_rejected(self):
        with self.assertRaises(ValueError):
            save_supplier(self.store, ACTIVE_NAME, EMAIL, "01164960000")


class TestPhoneDigitBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def save(self, phone):
        return save_supplier(self.store, NEW_NAME, EMAIL, phone)

    def test_six_digits_is_rejected(self):
        before = snapshot(self.store)
        with self.assertRaises(ValueError):
            self.save("123456")
        self.assertEqual(self.store, before)

    def test_seven_digits_is_accepted(self):
        self.assertEqual(self.save("1234567").phone, "1234567")

    def test_eight_digits_is_accepted(self):
        self.assertEqual(self.save("12345678").phone, "12345678")

    def test_fourteen_digits_is_accepted(self):
        self.assertEqual(self.save("12345678901234").phone, "12345678901234")

    def test_fifteen_digits_is_accepted(self):
        self.assertEqual(self.save("+123456789012345").phone,
                         "+123456789012345")

    def test_sixteen_digits_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("1234567890123456")

    def test_six_digits_with_plus_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("+123456")

    def test_empty_phone_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("")


class TestEmailBoundary(unittest.TestCase):

    def setUp(self):
        self.store = make_store()

    def save(self, email):
        return save_supplier(self.store, NEW_NAME, email, "01164960000")

    def test_shortest_valid_email_is_accepted(self):
        self.assertEqual(self.save("a@b.c").email, "a@b.c")

    def test_missing_local_part_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("@b.co")

    def test_missing_domain_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("a@.co")

    def test_missing_top_level_part_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("a@b.")

    def test_two_at_signs_are_rejected(self):
        with self.assertRaises(ValueError):
            self.save("a@@b.co")

    def test_empty_email_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save("")


class TestIdSequenceBoundary(unittest.TestCase):

    def test_first_supplier_in_empty_store_is_sup0001(self):
        from stock_control.store import Store
        store = Store()
        self.assertEqual(
            save_supplier(store, NEW_NAME, EMAIL, "01164960000").supplier_id,
            "SUP0001")


if __name__ == "__main__":
    unittest.main()
