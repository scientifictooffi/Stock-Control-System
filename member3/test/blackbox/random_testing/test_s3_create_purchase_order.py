import random
import unittest
from datetime import date, timedelta

from member3.test.s3_fixtures import (
    ACME, BRICK_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, snapshot)
from stock_control.purchasing.orders import create_purchase_order

SEED = 7095
RUNS = 600
SUPPLIERS = [ACME, ACME, DELTA, DELTA, DELTA, SUSPENDED_ID, UNKNOWN_ID]
SKUS = [PIPE_SKU, PIPE_SKU, TAP_SKU, BRICK_SKU, BRICK_SKU, UNKNOWN_SKU]
BAD_QUANTITIES = [0, -1, -20, 2.5, "4", None, True]
BAD_DATES = ["07/11/2026", "2026-13-01", "2026-02-30", "", "tomorrow",
             "20261107", None]


def random_date(rng):
    return (date(2026, 1, 1) + timedelta(days=rng.randint(0, 800))).isoformat()


def random_inputs(rng):
    supplier = rng.choice(SUPPLIERS)
    lines = []
    for _ in range(rng.choice([0, 1, 1, 2, 2, 3, 4])):
        quantity = (rng.randint(1, 40) if rng.random() < 0.85
                    else rng.choice(BAD_QUANTITIES))
        lines.append((rng.choice(SKUS), quantity))
    day = random_date(rng) if rng.random() < 0.9 else rng.choice(BAD_DATES)
    return supplier, lines, day


def is_date(text):
    try:
        return date.fromisoformat(text).isoformat() == text
    except (TypeError, ValueError):
        return False


def expected_outcome(store, supplier_id, lines, day):
    """Return (error, ex_pence). The model works in whole pence."""
    if supplier_id not in store.suppliers:
        return KeyError, None
    supplier = store.suppliers[supplier_id]
    if supplier.status != "active" or not lines or not is_date(day):
        return ValueError, None
    prices = {x.sku: x.price for x in store.product_suppliers
              if x.supplier_id == supplier_id}
    seen = set()
    pence = 0
    for sku, quantity in lines:
        if sku not in prices or sku in seen:
            return ValueError, None
        if type(quantity) is not int or quantity <= 0:
            return ValueError, None
        seen.add(sku)
        pence += quantity * round(prices[sku] * 100)
    if pence < round(supplier.min_order_value * 100):
        return ValueError, None
    return None, pence


class TestCreatePurchaseOrderRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        store = make_store()
        accepted = refused = 0
        for run in range(RUNS):
            args = random_inputs(rng)
            expected, pence = expected_outcome(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if expected is None:
                    order = create_purchase_order(store, *args)
                    inc_pence = (pence * 12 + 5) // 10
                    self.assertEqual(order.total_ex_vat, pence / 100)
                    self.assertEqual(order.total_inc_vat, inc_pence / 100)
                    self.assertEqual(order.status, "draft")
                    self.assertEqual(len(order.lines), len(args[1]))
                    self.assertEqual(
                        len(store.purchase_orders),
                        len(before.purchase_orders) + 1)
                    accepted += 1
                else:
                    with self.assertRaises(expected):
                        create_purchase_order(store, *args)
                    self.assertEqual(store, before)
                    refused += 1
        self.assertGreater(accepted, 30)
        self.assertGreater(refused, 30)

    def test_order_ids_are_unique_and_in_sequence(self):
        rng = random.Random(SEED)
        store = make_store()
        for _ in range(RUNS):
            try:
                create_purchase_order(store, *random_inputs(rng))
            except (ValueError, KeyError):
                pass
        ids = list(store.purchase_orders)
        self.assertGreater(len(ids), 10)
        self.assertEqual(ids, [f"PO{n:04d}" for n in range(1, len(ids) + 1)])


if __name__ == "__main__":
    unittest.main()
