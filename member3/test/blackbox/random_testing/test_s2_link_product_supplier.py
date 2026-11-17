import random
import unittest

from member3.test.s2_fixtures import (
    ACME, ARCHIVED_SKU, DELTA, PIPE_SKU, SUSPENDED_ID, TAP_SKU, UNKNOWN_ID,
    UNKNOWN_SKU, make_store, snapshot)
from stock_control.purchasing.suppliers import link_product_supplier

SEED = 7095
RUNS = 600
SKUS = [PIPE_SKU, PIPE_SKU, TAP_SKU, TAP_SKU, ARCHIVED_SKU, UNKNOWN_SKU]
SUPPLIERS = [ACME, ACME, DELTA, DELTA, SUSPENDED_ID, UNKNOWN_ID]
BAD_PRICES = [0, -1, -0.01, "5", None, True, float("inf"), float("nan")]
BAD_LEADS = [0, -5, 91, 365, 7.5, "7", None, True]
BAD_PACKS = [0, -1, 2.5, "3", None, True]


def random_inputs(rng):
    sku = rng.choice(SKUS)
    supplier = rng.choice(SUPPLIERS)
    price = (round(rng.uniform(0.01, 500), 2) if rng.random() < 0.8
             else rng.choice(BAD_PRICES))
    lead = rng.randint(1, 90) if rng.random() < 0.8 else rng.choice(BAD_LEADS)
    preferred = rng.random() < 0.35
    pack = rng.randint(1, 50) if rng.random() < 0.9 else rng.choice(BAD_PACKS)
    return sku, supplier, price, lead, preferred, pack


def is_whole(value):
    return type(value) is int


def expected_outcome(store, sku, supplier, price, lead, preferred, pack):
    if sku not in store.products:
        return KeyError
    if store.products[sku].status != "active":
        return ValueError
    if supplier not in store.suppliers:
        return KeyError
    if store.suppliers[supplier].status != "active":
        return ValueError
    if (type(price) not in (int, float) or price != price
            or price in (float("inf"), float("-inf")) or price <= 0):
        return ValueError
    if not is_whole(lead) or not 1 <= lead <= 90:
        return ValueError
    if not is_whole(pack) or pack < 1:
        return ValueError
    if preferred and any(
            x.sku == sku and x.preferred and x.supplier_id != supplier
            for x in store.product_suppliers):
        return ValueError
    return None


class TestLinkProductSupplierRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        store = make_store()
        accepted = refused = 0
        for run in range(RUNS):
            args = random_inputs(rng)
            expected = expected_outcome(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if expected is None:
                    link = link_product_supplier(
                        store, args[0], args[1], args[2], args[3],
                        args[4], args[5])
                    self.assertIn(link, store.product_suppliers)
                    self.assertEqual(
                        (link.price, link.lead_time_days, link.pack_size,
                         link.preferred),
                        (args[2], args[3], args[5], args[4]))
                    accepted += 1
                else:
                    with self.assertRaises(expected):
                        link_product_supplier(
                            store, args[0], args[1], args[2], args[3],
                            args[4], args[5])
                    self.assertEqual(store, before)
                    refused += 1
                self.assert_invariants(store)
        self.assertGreater(accepted, 30)
        self.assertGreater(refused, 30)

    def assert_invariants(self, store):
        pairs = [(x.sku, x.supplier_id) for x in store.product_suppliers]
        self.assertEqual(len(pairs), len(set(pairs)))
        for sku, product in store.products.items():
            preferred = [x.supplier_id for x in store.product_suppliers
                         if x.sku == sku and x.preferred]
            self.assertLessEqual(len(preferred), 1)
            self.assertEqual(
                product.preferred_supplier,
                preferred[0] if preferred else None)


if __name__ == "__main__":
    unittest.main()
