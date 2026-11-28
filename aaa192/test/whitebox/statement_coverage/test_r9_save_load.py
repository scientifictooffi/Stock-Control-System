"""R9 save_data / load_data - white-box: statement coverage.

Every statement in storage.py runs at least once.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestSaveLoadStatementCoverage(FileTestCase):

    def test_save_not_a_store(self):
        with self.assertRaises(ValueError):
            save_data("store", self.data_file)

    def test_save_twice_copies_backup(self):
        save_data(make_store(), self.data_file)
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))

    def test_load_no_files(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_load_backup_when_file_not_json(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "not json")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_file_cannot_be_read(self):
        os.mkdir(self.data_file)
        with self.assertRaisesRegex(ValueError,
                                    r"stock\.json \(file cannot be read"):
            load_data(self.data_file)

    def test_file_not_an_object(self):
        self.write_text(self.data_file, "[1, 2]")
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)

    def test_file_wrong_layout(self):
        self.write_text(self.data_file, '{"users": {"a": "b"}}')
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)


if __name__ == "__main__":
    unittest.main()
