import random
import unittest
from bpt5.test.m3_fixtures import SKU, TODAY, UNKNOWN_SKU, snapshot
from stock_control.models import Product, User, Warehouse
from stock_control.movements.adjustments import adjust_stock
from stock_control.store import Store

SEED = 7095
RUNS = 500
REASONS = ["damaged", "lost", "count error", "count error", "stolen", ""]
WAREHOUSES = ["MAIN", "MAIN", "MAIN", "NORTH", "EAST"]
APPROVERS = [None, None, "kim", "sam", "lee", "bob"]
BAD_CHANGES = [0, 2.5, "3", None, True]


def random_store(rng):
    store = Store()
    store.warehouses = {"MAIN": Warehouse("MAIN", "Main"),
                        "NORTH": Warehouse("NORTH", "North")}
    stock = rng.randint(0, 200)
    cost = rng.choice([0.0, 1.5, 6.0, 49.99, 120.0, 250.0])
    store.products[SKU] = Product(SKU, "Pipe", "Plumbing", 9.99, cost=cost,
                                  quantity=stock,
                                  stock_by_warehouse={"MAIN": stock})
    store.users = {"kim": User("kim", "p", "manager"),
                   "sam": User("sam", "p", "staff"),
                   "lee": User("lee", "p", "manager", active=False)}
    return store


def random_request(rng):
    sku = SKU if rng.random() < 0.9 else UNKNOWN_SKU
    if rng.random() < 0.85:
        change = rng.choice([-1, 1]) * rng.randint(1, 60)
    else:
        change = rng.choice(BAD_CHANGES)
    return (sku, change, rng.choice(REASONS), rng.choice(WAREHOUSES), TODAY,
            rng.choice(APPROVERS))


def expected_error(store, sku, change, reason, warehouse, day, approver):
    if sku not in store.products:
        return KeyError
    if reason not in ("damaged", "lost", "count error"):
        return ValueError
    if type(change) is not int or change == 0:
        return ValueError
    if warehouse not in store.warehouses:
        return ValueError
    stock = store.products[sku].stock_by_warehouse.get(warehouse, 0)
    if stock + change < 0:
        return ValueError
    over_percent = abs(change) / stock > 0.10 if stock else True
    over_value = round(abs(change) * store.products[sku].cost, 2) > 500
    if (over_percent or over_value) and approver != "kim":
        return ValueError
    return None


class TestAdjustStockRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        accepted = refused = 0
        for run in range(RUNS):
            store = random_store(rng)
            args = random_request(rng)
            error = expected_error(store, *args)
            before = snapshot(store)
            with self.subTest(run=run, args=args):
                if error is not None:
                    with self.assertRaises(error):
                        adjust_stock(store, *args)
                    self.assertEqual(store, before)
                    refused += 1
                    continue
                warehouse, change = args[3], args[1]
                old = before.products[SKU].stock_by_warehouse.get(
                    warehouse, 0)
                self.assertEqual(adjust_stock(store, *args), old + change)
                product = store.products[SKU]
                self.assertGreaterEqual(product.stock_by_warehouse[warehouse],
                                        0)
                self.assertEqual(product.quantity,
                                 before.products[SKU].quantity + change)
                self.assertEqual(store.movements[-1].quantity, change)
                accepted += 1
        self.assertGreater(accepted, 30)
        self.assertGreater(refused, 30)


if __name__ == "__main__":
    unittest.main()
