import random
import unittest
from datetime import date, timedelta
from member2.test.m2_fixtures import SKU, TODAY, UNKNOWN_SKU, snapshot
from stock_control.models import Batch, Product, Warehouse
from stock_control.movements.issuing import issue_stock
from stock_control.store import Store

SEED = 7095
RUNS = 500
WAREHOUSES = ["MAIN", "MAIN", "MAIN", "NORTH", "EAST"]
BAD_QUANTITIES = [0, -1, 2.5, "4", None, True]


def random_day(rng):
    return (date(2026, 10, 1) + timedelta(days=rng.randint(0, 120))
            ).isoformat()

def random_store(rng):
    store = Store()
    store.warehouses = {"MAIN": Warehouse("MAIN", "Main"),
                        "NORTH": Warehouse("NORTH", "North")}
    batches = []
    for number in range(rng.randint(0, 5)):
        use_by = random_day(rng) if rng.random() < 0.8 else None
        batches.append(Batch(f"B{number + 1:04d}", SKU, "MAIN",
                             rng.randint(1, 6), random_day(rng), use_by))
    batches.append(Batch("B0099", "TAP-0001", "MAIN", 3, "2026-10-01",
                         "2026-10-02"))
    in_batches = sum(b.quantity for b in batches if b.sku == SKU)
    main = in_batches + rng.randint(0, 3)
    store.products[SKU] = Product(SKU, "Pipe", "Plumbing", 9.99,
                                  quantity=main,
                                  stock_by_warehouse={"MAIN": main})
    store.batches = batches
    return store


def random_request(rng):
    sku = SKU if rng.random() < 0.9 else UNKNOWN_SKU
    if rng.random() < 0.8:
        quantity = rng.randint(1, 30)
    else:
        quantity = rng.choice(BAD_QUANTITIES)
    return sku, quantity, rng.choice(WAREHOUSES), TODAY, rng.random() < 0.5


def expected_outcome(store, sku, quantity, warehouse, day, partial):
    if sku not in store.products:
        return KeyError, None
    if type(quantity) is not int or quantity <= 0:
        return ValueError, None
    if warehouse not in store.warehouses:
        return ValueError, None
    available = store.products[sku].stock_by_warehouse.get(warehouse, 0)
    if quantity <= available:
        return None, quantity
    if not partial or available == 0:
        return ValueError, None
    return None, available


def expected_batches(store, sku, warehouse, amount):
    own = [b for b in store.batches
           if b.sku == sku and b.warehouse == warehouse and b.quantity > 0]
    own.sort(key=lambda b: (b.use_by_date or "9999-12-31", b.received_date))
    left = {b.batch_id: b.quantity for b in store.batches}
    for b in own:
        taken = min(left[b.batch_id], amount)
        left[b.batch_id] -= taken
        amount -= taken
    return left


class TestIssueStockRandom(unittest.TestCase):

    def test_random_requests_follow_the_rules(self):
        rng = random.Random(SEED)
        accepted = refused = 0
        for run in range(RUNS):
            store = random_store(rng)
            args = random_request(rng)
            error, issued = expected_outcome(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if error is not None:
                    with self.assertRaises(error):
                        issue_stock(store, *args)
                    self.assertEqual(store, before)
                    refused += 1
                    continue
                want = expected_batches(store, SKU, args[2], issued)
                self.assertEqual(issue_stock(store, *args), issued)
                product = store.products[SKU]
                self.assertEqual(
                    product.stock_by_warehouse[args[2]],
                    before.products[SKU].stock_by_warehouse.get(args[2], 0)
                    - issued)
                self.assertGreaterEqual(product.quantity, 0)
                self.assertGreaterEqual(
                    min(product.stock_by_warehouse.values()), 0)
                self.assertEqual(
                    {b.batch_id: b.quantity for b in store.batches}, want)
                self.assertEqual(len(store.movements), 1)
                accepted += 1
        self.assertGreater(accepted, 50)
        self.assertGreater(refused, 50)


if __name__ == "__main__":
    unittest.main()
