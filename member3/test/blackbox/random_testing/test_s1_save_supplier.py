import random
import re
import unittest

from member3.test.s1_fixtures import (
    ACTIVE_ID, SUSPENDED_ID, UNKNOWN_ID, make_store, snapshot)
from stock_control.purchasing.suppliers import save_supplier

SEED = 7095
RUNS = 500
EMAIL_RE = re.compile(r"^[^@\s]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
PHONE_RE = re.compile(r"^\+?[0-9 ()-]+$")
GOOD_NAMES = ["Acme Plumbing Ltd", "acme plumbing ltd", "Delta Tools",
              "Zed Ltd", "Kappa Supplies", "Omega Bricks"]
BAD_NAMES = ["", "   ", None, 42]
GOOD_EMAILS = ["a@b.co", "buyer@omega.co.uk", "x.y@z-1.com"]
BAD_EMAILS = ["bad", "a@b", "@b.co", "a b@c.de", "", None, 7]
GOOD_PHONES = ["0116 496 0000", "+44 116 496 0000", "(0116) 4960000",
               "1234567"]
BAD_PHONES = ["123456", "12345678901234567", "abc", "01164960000x", "", None]
GOOD_STATUSES = ["active", "suspended"]
BAD_STATUSES = ["closed", "ACTIVE", "", None]
IDS = [None, None, None, ACTIVE_ID, SUSPENDED_ID, UNKNOWN_ID]
GOOD_SHARE = 0.85


def pick(rng, good, bad):
    return rng.choice(good) if rng.random() < GOOD_SHARE else rng.choice(bad)


def random_inputs(rng):
    return (pick(rng, GOOD_NAMES, BAD_NAMES),
            pick(rng, GOOD_EMAILS, BAD_EMAILS),
            pick(rng, GOOD_PHONES, BAD_PHONES),
            pick(rng, GOOD_STATUSES, BAD_STATUSES),
            rng.choice(IDS))


def valid_email(value):
    return isinstance(value, str) and EMAIL_RE.match(value.strip()) is not None


def valid_phone(value):
    if not isinstance(value, str) or PHONE_RE.match(value.strip()) is None:
        return False
    return 7 <= sum(c.isdigit() for c in value) <= 15


def expected_outcome(store, name, email, phone, status, supplier_id):
    existing = None
    if supplier_id is not None:
        if supplier_id not in store.suppliers:
            return KeyError
        existing = store.suppliers[supplier_id]
    if not isinstance(name, str) or name.strip() == "":
        return ValueError
    clean = name.strip().casefold()
    for other_id, other in store.suppliers.items():
        if other_id != supplier_id and other.name.casefold() == clean:
            return ValueError
    if not valid_email(email) or not valid_phone(phone):
        return ValueError
    if status not in ("active", "suspended"):
        return ValueError
    if existing is not None and existing.status == "suspended":
        if status != "active":
            return ValueError
        if (name.strip(), email.strip(), phone.strip()) != (
                existing.name, existing.email, existing.phone):
            return ValueError
    return None


class TestSaveSupplierRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        accepted = refused = 0
        for run in range(RUNS):
            store = make_store()
            args = random_inputs(rng)
            expected = expected_outcome(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if expected is None:
                    supplier = save_supplier(
                        store, args[0], args[1], args[2], args[3], args[4])
                    self.assertEqual(supplier.status, args[3])
                    self.assertEqual(supplier.name, args[0].strip())
                    self.assertIs(
                        store.suppliers[supplier.supplier_id], supplier)
                    if args[4] is None:
                        self.assertEqual(
                            len(store.suppliers), len(before.suppliers) + 1)
                    else:
                        self.assertEqual(
                            len(store.suppliers), len(before.suppliers))
                    accepted += 1
                else:
                    with self.assertRaises(expected):
                        save_supplier(store, *args[:4], args[4])
                    self.assertEqual(store, before)
                    refused += 1
        self.assertGreater(accepted, 20)
        self.assertGreater(refused, 20)

    def test_names_stay_unique_after_many_random_saves(self):
        rng = random.Random(SEED)
        store = make_store()
        for _ in range(RUNS):
            args = random_inputs(rng)
            try:
                save_supplier(store, *args)
            except (ValueError, KeyError):
                pass
            names = [s.name.casefold() for s in store.suppliers.values()]
            self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
