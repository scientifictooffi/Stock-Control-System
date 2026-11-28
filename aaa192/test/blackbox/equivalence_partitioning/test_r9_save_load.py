"""R9 save_data / load_data - black-box: equivalence partitioning.

One test per input class (store valid or not, file missing, good or
damaged, backup good or damaged).
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestSaveDataEquivalencePartitioning(FileTestCase):

    def test_ec1_first_save_json_and_no_backup(self):
        save_data(make_store(), self.data_file)
        data = self.read_json(self.data_file)
        self.assertEqual("Hammer", data["products"]["TLS-0001"]["name"])
        self.assertFalse(os.path.exists(self.backup_file))

    def test_ec2_not_a_store(self):
        for bad in (None, {"products": {}}):
            with self.subTest(store=bad):
                with self.assertRaisesRegex(ValueError, "must be a Store"):
                    save_data(bad, self.data_file)
        self.assertFalse(os.path.exists(self.data_file))

    def test_ec3_good_file_becomes_backup(self):
        save_data(make_store(), self.data_file)
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_ec4_damaged_file_not_copied_to_backup(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "{damaged")
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))


class TestLoadDataEquivalencePartitioning(FileTestCase):

    def test_ec5_no_files_starts_empty(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_ec6_good_file(self):
        save_data(make_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_ec7_damaged_file_loads_backup(self):
        self.save_good(self.backup_file, make_store())
        for text in ("{damaged", "[]", '{"products": []}'):
            with self.subTest(text=text):
                self.write_text(self.data_file, text)
                self.assertEqual(make_store(), load_data(self.data_file))

    def test_ec8_missing_file_loads_backup(self):
        self.save_good(self.backup_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_ec9_both_damaged_clear_error(self):
        self.write_text(self.data_file, "{damaged")
        self.write_text(self.backup_file, "also damaged")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)


if __name__ == "__main__":
    unittest.main()
