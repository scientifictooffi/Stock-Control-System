"""R9 save_data / load_data - white-box: condition testing.

load_data has one decision with two simple conditions:
    not os.path.exists(file_path) and not os.path.exists(backup)
A = the data file is missing, B = the backup is missing.
All 2^2 = 4 combinations are possible, so there is one test for each.
Every other decision in storage.py has a single condition; each one is
also made True and False (tests 5-9).
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestLoadDataConditionTesting(FileTestCase):

    # 1. (T, T) -> no data file, no backup: start with an empty store
    def test_both_missing(self):
        self.assertEqual(Store(), load_data(self.data_file))

    # 2. (T, F) -> no data file, backup there: the backup is loaded
    def test_data_missing_backup_there(self):
        self.save_good(self.backup_file, other_store())
        self.assertEqual(other_store(), load_data(self.data_file))

    # 3. (F, T) -> data file there, no backup: the data file is loaded
    def test_data_there_backup_missing(self):
        self.save_good(self.data_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    # 4. (F, F) -> both there: the data file is loaded, not the backup
    def test_both_there(self):
        self.save_good(self.data_file, make_store())
        self.save_good(self.backup_file, other_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    # 5. store is not a Store: T (refused) and F (saved)
    def test_store_is_not_a_store(self):
        with self.assertRaises(ValueError):
            save_data(None, self.data_file)
        save_data(Store(), self.data_file)
        self.assertEqual(Store(), load_data(self.data_file))

    # 6. data file can be read before saving: T (copied to backup)
    #    and F (damaged, backup left alone)
    def test_data_file_can_be_read_before_save(self):
        self.save_good(self.data_file, make_store())
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))
        self.write_text(self.data_file, "{x")
        save_data(Store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))

    # 7. data file fails to load: T, then backup fails to load: T and F
    def test_data_and_backup_fail_to_load(self):
        self.write_text(self.data_file, "{x")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)
        self.save_good(self.backup_file, other_store())
        self.assertEqual(other_store(), load_data(self.data_file))

    # 8. file cannot be opened: T (a folder)
    def test_cannot_open_and_not_json(self):
        os.mkdir(self.data_file)
        with self.assertRaisesRegex(ValueError, "cannot be read"):
            load_data(self.data_file)

    # 9. top level is not an object: T, and a row does not match: T
    def test_not_an_object_and_row_not_matching(self):
        for text in ("[]", '{"products": []}'):
            with self.subTest(text=text):
                self.write_text(self.data_file, text)
                with self.assertRaisesRegex(ValueError,
                                            "does not hold saved data"):
                    load_data(self.data_file)


if __name__ == "__main__":
    unittest.main()
