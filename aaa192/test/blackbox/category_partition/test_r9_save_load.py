"""R9 save_data / load_data - black-box: category partition (Lab 8).

One test per frame in r9_save_load.frames.txt, made by TSLgenerator
from r9_save_load.tsl.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestSaveLoadCategoryPartition(FileTestCase):

    def given_files(self, data, backup):
        """Set up the two files. Each one is "missing", "saved earlier"
        (make_store() for the data file, other_store() for the backup)
        or "not valid JSON"."""
        for path, state, store in ((self.data_file, data, make_store()),
                                   (self.backup_file, backup,
                                    other_store())):
            if state == "saved earlier":
                self.save_good(path, store)
            elif state == "not valid JSON":
                self.write_text(path, "{damaged")

    # Single and error frames

    def test_frame_01_store_not_a_store_error(self):
        with self.assertRaises(ValueError):
            save_data([], self.data_file)

    def test_frame_02_empty_store(self):
        save_data(Store(), self.data_file)
        self.assertEqual(Store(), load_data(self.data_file))

    def test_frame_03_data_file_empty(self):
        self.given_files("missing", "saved earlier")
        self.write_text(self.data_file, "")
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_frame_04_data_file_json_but_not_saved_data(self):
        self.given_files("missing", "saved earlier")
        for text in ("[]", '{"products": []}'):
            with self.subTest(text=text):
                self.write_text(self.data_file, text)
                self.assertEqual(other_store(), load_data(self.data_file))

    def test_frame_05_backup_damaged(self):
        self.given_files("not valid JSON", "not valid JSON")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    # save_data frames: Store with data

    def test_frame_06_save_no_data_file_no_backup(self):
        self.given_files("missing", "missing")
        save_data(make_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.data_file))
        self.assertFalse(os.path.exists(self.backup_file))

    def test_frame_07_save_no_data_file_backup_kept(self):
        self.given_files("missing", "saved earlier")
        save_data(make_store(), self.data_file)
        self.assertEqual(other_store(), load_data(self.backup_file))

    def test_frame_08_save_data_file_becomes_backup(self):
        self.given_files("saved earlier", "missing")
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_frame_09_save_data_file_replaces_backup(self):
        self.given_files("saved earlier", "saved earlier")
        save_data(Store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))

    def test_frame_10_save_damaged_file_no_backup(self):
        self.given_files("not valid JSON", "missing")
        save_data(make_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.data_file))
        self.assertFalse(os.path.exists(self.backup_file))

    def test_frame_11_save_damaged_file_backup_kept(self):
        self.given_files("not valid JSON", "saved earlier")
        save_data(make_store(), self.data_file)
        self.assertEqual(other_store(), load_data(self.backup_file))

    # load_data frames

    def test_frame_12_load_no_files_starts_empty(self):
        self.given_files("missing", "missing")
        self.assertEqual(Store(), load_data(self.data_file))

    def test_frame_13_load_missing_file_uses_backup(self):
        self.given_files("missing", "saved earlier")
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_frame_14_load_good_file_no_backup(self):
        self.given_files("saved earlier", "missing")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_frame_15_load_good_file_backup_not_used(self):
        self.given_files("saved earlier", "saved earlier")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_frame_16_load_damaged_file_no_backup_error(self):
        self.given_files("not valid JSON", "missing")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    def test_frame_17_load_damaged_file_uses_backup(self):
        self.given_files("not valid JSON", "saved earlier")
        self.assertEqual(other_store(), load_data(self.data_file))


if __name__ == "__main__":
    unittest.main()
