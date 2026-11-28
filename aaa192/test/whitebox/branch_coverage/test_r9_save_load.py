"""R9 save_data / load_data - white-box: branch coverage.

Every decision in storage.py is tested True and False.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestSaveLoadBranchCoverage(FileTestCase):

    def test_d1_true_not_a_store(self):
        with self.assertRaises(ValueError):
            save_data(None, self.data_file)

    def test_d1_false_d3_false_first_save(self):
        save_data(make_store(), self.data_file)
        self.assertFalse(os.path.exists(self.backup_file))

    def test_d3_true_backup_copied(self):
        save_data(make_store(), self.data_file)
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))

    def test_d4_true_no_files(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_d4_false_d5_false_good_file(self):
        save_data(make_store(), self.data_file)
        loaded = load_data(self.data_file)
        self.assertEqual(make_store(), loaded)
        self.assertEqual(2, len(loaded.purchase_orders["PO0001"].lines))

    def test_d5_true_d6_false_backup_used(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "{")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_d5_true_d6_true_both_fail(self):
        self.write_text(self.data_file, "{")
        self.write_text(self.backup_file, "{")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    def test_d7_true_cannot_open(self):
        os.mkdir(self.data_file)
        with self.assertRaisesRegex(ValueError,
                                    r"stock\.json \(file cannot be read"):
            load_data(self.data_file)

    def test_d8_true_not_json(self):
        self.write_text(self.data_file, "hello")
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            load_data(self.data_file)

    def test_d9_true_not_an_object(self):
        self.write_text(self.data_file, '"text"')
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)

    def test_d11_true_dict_collection_given_a_list(self):
        self.write_text(self.data_file, '{"products": []}')
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)


if __name__ == "__main__":
    unittest.main()
