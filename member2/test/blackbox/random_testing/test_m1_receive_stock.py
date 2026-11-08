import random
import unittest
from datetime import date, timedelta

from member2.test.m1_fixtures import (
    ACTIVE_SKU, ARCHIVED_SKU, UNKNOWN_SKU, make_store, snapshot)
from stock_control.movements.receiving import receive_stock

SEED = 7095
RUNS = 500
SKUS = [ACTIVE_SKU, ACTIVE_SKU, ACTIVE_SKU, ARCHIVED_SKU, UNKNOWN_SKU]
WAREHOUSES = ["MAIN", "NORTH", "MAIN", "EAST", ""]
BAD_QUANTITIES = [0, -1, -50, 2.5, "10", None, True]
BAD_DATES = ["07/11/2026", "2026-13-01", "2026-02-30", "", "tomorrow",
             "20261107", "2026-W45-6"]


def random_date(rng):
    start = date(2026, 1, 1)
    return (start + timedelta(days=rng.randint(0, 800))).isoformat()


def random_inputs(rng):
    sku = rng.choice(SKUS)
    if rng.random() < 0.7:
        quantity = rng.randint(1, 5000)
    else:
        quantity = rng.choice(BAD_QUANTITIES)
    warehouse = rng.choice(WAREHOUSES)
    day = random_date(rng) if rng.random() < 0.9 else rng.choice(BAD_DATES)
    pick = rng.random()
    if pick < 0.3:
        use_by = None
    elif pick < 0.9:
        use_by = random_date(rng)
    else:
        use_by = rng.choice(BAD_DATES)
    return sku, quantity, warehouse, day, use_by


def is_date(text):
    try:
        return date.fromisoformat(text).isoformat() == text
    except (TypeError, ValueError):
        return False


def expected_outcome(store, sku, quantity, warehouse, day, use_by):
    if sku not in store.products:
        return KeyError
    if store.products[sku].status != "active":
        return ValueError
    if type(quantity) is not int or quantity <= 0:
        return ValueError
    if warehouse not in store.warehouses:
        return ValueError
    if not is_date(day):
        return ValueError
    if use_by is not None and (not is_date(use_by) or use_by < day):
        return ValueError
    return None


class TestReceiveStockRandom(unittest.TestCase):

    def test_random_inputs_match_the_rules(self):
        rng = random.Random(SEED)
        store = make_store()
        accepted = refused = 0
        for run in range(RUNS):
            args = random_inputs(rng)
            expected = expected_outcome(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if expected is None:
                    sku, quantity = args[0], args[1]
                    old_total = store.products[sku].quantity
                    result = receive_stock(store, *args)
                    self.assertEqual(result, old_total + quantity)
                    self.assertEqual(len(store.batches),
                                     len(before.batches) + 1)
                    self.assertEqual(len(store.movements),
                                     len(before.movements) + 1)
                    accepted += 1
                else:
                    with self.assertRaises(expected):
                        receive_stock(store, *args)
                    self.assertEqual(store, before)
                    refused += 1
                for product in store.products.values():
                    self.assertEqual(
                        product.quantity,
                        sum(product.stock_by_warehouse.values()))
        self.assertGreater(accepted, 20)
        self.assertGreater(refused, 20)


if __name__ == "__main__":
    unittest.main()
