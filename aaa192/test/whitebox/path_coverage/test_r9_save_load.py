"""R9 save_data / load_data - white-box: path coverage.

One test per path through save_data, load_data, _read_store and _build.
"""
import os
import unittest

from aaa192.test.r9_fixtures import FileTestCase, make_store, other_store
from stock_control.models import Category
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store


class TestSaveLoadPathCoverage(FileTestCase):

    def test_path_p1_not_a_store(self):
        with self.assertRaisesRegex(ValueError, "must be a Store"):
            save_data(42, self.data_file)

    def test_path_p2_write_no_backup(self):
        save_data(make_store(), self.data_file)
        self.assertTrue(os.path.exists(self.data_file))
        self.assertFalse(os.path.exists(self.backup_file))

    def test_path_p3_backup_then_write(self):
        save_data(make_store(), self.data_file)
        save_data(other_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.backup_file))
        self.assertEqual(other_store(), load_data(self.data_file))

    def test_path_p4_empty_store(self):
        self.assertEqual(Store(), load_data(self.data_file))

    def test_path_p5_data_file(self):
        save_data(make_store(), self.data_file)
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_path_p6_backup_data_file_missing(self):
        self.save_good(self.backup_file, make_store())
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_path_p6_backup_data_file_damaged(self):
        self.save_good(self.backup_file, make_store())
        self.write_text(self.data_file, "{oops")
        self.assertEqual(make_store(), load_data(self.data_file))

    def test_path_p7_both_fail(self):
        self.write_text(self.data_file, "{oops")
        with self.assertRaisesRegex(ValueError, "could not load the data"):
            load_data(self.data_file)

    def test_path_q1_cannot_be_read(self):
        os.mkdir(self.data_file)
        with self.assertRaisesRegex(ValueError,
                                    r"stock\.json \(file cannot be read"):
            load_data(self.data_file)

    def test_path_q2_not_json(self):
        self.write_text(self.data_file, "{oops")
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            load_data(self.data_file)

    def test_path_q3_not_an_object(self):
        self.write_text(self.data_file, "12")
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)

    def test_path_q4_wrong_layout(self):
        self.write_text(self.data_file, '{"movements": 5}')
        with self.assertRaisesRegex(ValueError, "does not hold saved"):
            load_data(self.data_file)

    def test_path_q5_good_layout(self):
        self.write_text(self.data_file,
                        '{"categories": {"Tools": {"name": "Tools"}}}')
        self.assertEqual({"Tools": Category("Tools")},
                         load_data(self.data_file).categories)


if __name__ == "__main__":
    unittest.main()
