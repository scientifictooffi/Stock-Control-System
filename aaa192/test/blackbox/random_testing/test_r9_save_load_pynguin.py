"""R9 save_data / load_data - black-box: random testing with Pynguin.

Generated with Pynguin (Lab 9) using --algorithm RANDOM --seed 0
--maximum_iterations 60, then changed from pytest to unittest so it
runs with the other tests. Each test runs in a temporary folder
because Pynguin uses random file names.
"""
import os
import sys
import tempfile
import unittest

import stock_control.reporting.storage

storage_ = sys.modules["stock_control.reporting.storage"]


class TestSaveLoadPynguin(unittest.TestCase):

    def setUp(self):
        self._old_dir = os.getcwd()
        self._folder = tempfile.TemporaryDirectory()
        os.chdir(self._folder.name)

    def tearDown(self):
        os.chdir(self._old_dir)
        self._folder.cleanup()

    def test_0(self):
        storage_.backup_path(file_path="suppliers")

    def test_1(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_0)

    def test_2(self):
        storage_.backup_path(
            file_path='file does not hold saved data:Turn a YYYY-MM-DD string into a date, or raise ValueError.\n\n    The round-trip check keeps this strict on every Python version:\n    from 3.11 fromisoformat also accepts forms such as "20261107".\n    '  # noqa: E501
        )

    def test_3(self):
        storage_.backup_path(file_path="suppliers")

    def test_4(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        var_3 = storage_.load_data(file_path=var_2)
        storage_.save_data(store=var_3, file_path=var_2)

    def test_5(self):
        var_3 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_3)

    def test_6(self):
        var_1 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_1)

    def test_7(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store=set(), file_path=complex(103.6459, -2840.78))  # noqa: E501

    def test_8(self):
        with self.assertRaises(Exception):
            storage_.load_data(file_path=[])

    def test_9(self):
        with self.assertRaises(Exception):
            var_0 = int
            storage_.backup_path(file_path=var_0)

    def test_10(self):
        with self.assertRaises(Exception):
            storage_.load_data(
                file_path=b"\xff\xee}\x1bM\x8dJ\xb4\x1f\x8cU\xd0\xec\x8a4\xf6\xcc"  # noqa: E501
            )

    def test_11(self):
        with self.assertRaises(Exception):
            storage_.load_data(file_path=0.0)

    def test_12(self):
        with self.assertRaises(Exception):
            storage_.load_data(file_path=False)

    def test_13(self):
        with self.assertRaises(Exception):
            storage_.load_data(
                file_path={
                    "P3 (Member 1): As Alex, I want to remove products we no longer sell so\n    that staff stop offering them.\n\n    Rules:\n        1. Delete only if stock is 0 and it has no history\n        2. Otherwise archive it\n        3. Not allowed if it is on an open order\n    ": True,  # noqa: E501
                    "not enough stock in ": 3,
                    "M8 process_return is not implemented yet": "{sL",
                }
            )

    def test_14(self):
        var_0 = storage_.load_data
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_0, file_path=var_0)

    def test_15(self):
        with self.assertRaises(Exception):
            storage_.load_data(file_path=None)

    def test_16(self):
        with self.assertRaises(Exception):
            storage_.backup_path(file_path=None)

    def test_17(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store=(), file_path=False)

    def test_18(self):
        var_0 = bool
        with self.assertRaises(ValueError):
            storage_.save_data(store=-970, file_path=var_0)

    def test_19(self):
        var_0 = bool
        with self.assertRaises(ValueError):
            storage_.save_data(store=("@a0/o`Gkus>VM", 89.0, -314.0), file_path=var_0)  # noqa: E501

    def test_20(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store=[], file_path=b"\xfc\x03f\xf3\xad")

    def test_21(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store={True}, file_path=0)

    def test_22(self):
        with self.assertRaises(Exception):
            storage_.backup_path(file_path=None)

    def test_23(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_0)
        var_2 = storage_.backup_path(
            file_path='file does not hold saved data:Turn a YYYY-MM-DD string into a date, or raise ValueError.\n\n    The round-trip check keeps this strict on every Python version:\n    from 3.11 fromisoformat also accepts forms such as "20261107".\n    '  # noqa: E501
        )
        var_4 = float
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_2, file_path=var_4)

    def test_24(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_0)

    def test_25(self):
        storage_.backup_path(file_path="suppliers")
        with self.assertRaises(ValueError):
            storage_.save_data(store={"admin": False}, file_path=None)

    def test_26(self):
        var_4 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_4)

    def test_27(self):
        with self.assertRaises(Exception):
            storage_.backup_path(file_path={-912.12, "74ZRi!:|a]"})

    def test_28(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_2)
        var_4 = object
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_4, file_path=var_4)

    def test_29(self):
        with self.assertRaises(ValueError):
            storage_.save_data(
                store=(),
                file_path=[
                    818,
                    "batches$R1 (Member 4): As Sam in the office, I want each staff member to log in\n    with their own account so that only our staff can use the system.\n\n    Rules:\n        1. Username must exist\n        2. Password is checked\n        3. Account locks after 3 wrong tries\n        4. Locked or inactive accounts cannot log in\n\n    Returns the logged-in User. Raises ValueError when a rule fails.\n    A wrong password adds 1 to failed_logins; on the 3rd wrong try the\n    account is locked. A correct password resets failed_logins to 0.\n    $Copper pipe 15mm 3m",  # noqa: E501
                    "`&R#DeiS+SadR8cR",
                ],
            )

    def test_30(self):
        with self.assertRaises(Exception):
            storage_.load_data(file_path=-1)

    def test_31(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_0)

        def var_3(*args, **kwargs):
            return ""

        with self.assertRaises(ValueError):
            storage_.save_data(store=var_3, file_path=b"!\x07\xf75\\Uy\xf5J")

    def test_32(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_0)

    def test_33(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store=1915.52, file_path=True)

    def test_34(self):
        var_0 = storage_.save_data
        with self.assertRaises(ValueError):
            storage_.save_data(store={1125.63}, file_path=var_0)

    def test_35(self):
        storage_.backup_path(file_path="suppliers")

    def test_36(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_2)

    def test_37(self):
        var_1 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_1)

    def test_38(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        with self.assertRaises(ValueError):
            storage_.save_data(store=None, file_path=var_0)

    def test_39(self):
        var_3 = storage_.backup_path(file_path="suppliers")
        var_4 = storage_.load_data(file_path=var_3)
        storage_.save_data(store=var_4, file_path=var_3)

    def test_40(self):
        var_5 = storage_.backup_path(file_path="suppliers")
        var_6 = storage_.load_data(file_path=var_5)
        storage_.save_data(store=var_6, file_path=var_5)

    def test_41(self):
        var_0 = tuple
        with self.assertRaises(ValueError):
            storage_.save_data(store=(), file_path=var_0)

    def test_42(self):
        var_0 = storage_.backup_path(file_path="suppliers")
        var_6 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_6)
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_0, file_path=[3381.5, ":aE", False])

    def test_43(self):
        with self.assertRaises(ValueError):
            storage_.save_data(store=-160.08, file_path=-1764.73)

    def test_44(self):
        with self.assertRaises(Exception):
            var_0 = bool
            storage_.backup_path(file_path=var_0)

    def test_45(self):
        with self.assertRaises(Exception):
            var_0 = list
            storage_.backup_path(file_path=var_0)

    def test_46(self):
        var_4 = storage_.backup_path(file_path="suppliers")
        var_5 = storage_.load_data(file_path=var_4)
        storage_.save_data(store=var_5, file_path=var_4)

    def test_47(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        var_3 = storage_.load_data(file_path=var_2)
        storage_.save_data(store=var_3, file_path=var_2)

    def test_48(self):
        var_6 = storage_.backup_path(file_path="suppliers")
        var_7 = storage_.load_data(file_path=var_6)
        storage_.save_data(store=var_7, file_path=var_6)

    def test_49(self):
        var_1 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_1)

    def test_50(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        var_3 = storage_.load_data(file_path=var_2)
        storage_.save_data(store=var_3, file_path=var_2)

    def test_51(self):
        var_12 = storage_.backup_path(file_path="suppliers")
        var_13 = storage_.load_data(file_path=var_12)
        storage_.save_data(store=var_13, file_path=var_12)

    def test_52(self):
        var_2 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_2)
        var_4 = list
        with self.assertRaises(ValueError):
            storage_.save_data(store=None, file_path=var_4)

    def test_53(self):
        var_1 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_1)
        var_3 = storage_.backup_path(file_path="suppliers")
        var_4 = storage_.backup_path(file_path=var_3)
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_3, file_path=var_4)

    def test_54(self):
        var_12 = storage_.backup_path(file_path="suppliers")
        var_13 = storage_.load_data(file_path=var_12)
        storage_.save_data(store=var_13, file_path=var_12)

    def test_55(self):
        var_4 = storage_.backup_path(file_path="suppliers")
        var_7 = storage_.backup_path(file_path="suppliers")
        var_8 = storage_.load_data(file_path=var_7)
        storage_.save_data(store=var_8, file_path=var_7)
        var_21 = complex
        with self.assertRaises(ValueError):
            storage_.save_data(store=var_4, file_path=var_21)

    def test_56(self):
        var_3 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_3)

    def test_57(self):
        var_4 = storage_.backup_path(file_path="suppliers")
        storage_.load_data(file_path=var_4)

    def test_58(self):
        var_0 = float
        with self.assertRaises(ValueError):
            storage_.save_data(store=1994.22, file_path=var_0)


if __name__ == "__main__":
    unittest.main()
