import random
import unittest
from bpt5.test.m4_fixtures import SKU, TODAY, UNKNOWN_SKU, snapshot
from stock_control.models import Product, Transfer, Warehouse
from stock_control.movements.transfers import transfer_stock
from stock_control.store import Store

SEED = 7095
RUNS = 500
WAREHOUSES = ["MAIN", "MAIN", "NORTH", "NORTH", "EAST"]
BAD_QUANTITIES = [0, -1, 2.5, "3", None, True]
ACTIONS = ["create", "create", "dispatch", "receive", "cancel", "ship"]
STATUSES = ["pending", "in transit", "received", "cancelled"]
ALLOWED = {"dispatch": ("pending",), "receive": ("in transit",),
           "cancel": ("pending", "in transit")}


def random_store(rng):
    store = Store()
    store.warehouses = {"MAIN": Warehouse("MAIN", "Main"),
                        "NORTH": Warehouse("NORTH", "North")}
    main, north = rng.randint(0, 60), rng.randint(0, 60)
    store.products[SKU] = Product(
        SKU, "Pipe", "Plumbing", 9.99, quantity=main + north,
        stock_by_warehouse={"MAIN": main, "NORTH": north})
    if rng.random() < 0.8:
        moved = rng.randint(1, 20)
        store.transfers["TR0001"] = Transfer(
            "TR0001", SKU, moved, "MAIN", "NORTH", rng.choice(STATUSES))
    return store


def random_request(rng):
    action = rng.choice(ACTIONS)
    if action != "create":
        transfer_id = "TR0001" if rng.random() < 0.85 else "TR9999"
        return (None, None, None, None, action, transfer_id)
    sku = SKU if rng.random() < 0.9 else UNKNOWN_SKU
    if rng.random() < 0.85:
        quantity = rng.randint(1, 70)
    else:
        quantity = rng.choice(BAD_QUANTITIES)
    return (sku, quantity, rng.choice(WAREHOUSES), rng.choice(WAREHOUSES),
            action, None)


def expected_error(store, sku, quantity, source, target, action, tid):
    if action == "create":
        if sku not in store.products:
            return KeyError
        if type(quantity) is not int or quantity <= 0:
            return ValueError
        if source == target:
            return ValueError
        if source not in store.warehouses or target not in store.warehouses:
            return ValueError
        if quantity > store.products[sku].stock_by_warehouse.get(source, 0):
            return ValueError
        return None
    if action not in ALLOWED:
        return ValueError
    if tid not in store.transfers:
        return KeyError
    if store.transfers[tid].status not in ALLOWED[action]:
        return ValueError
    return None


class TestTransferStockRandom(unittest.TestCase):

    def check_success(self, store, before, args):
        sku, quantity, source, target, action, tid = args
        after = store.products[SKU].stock_by_warehouse
        old = before.products[SKU].stock_by_warehouse
        if action == "create":
            self.assertEqual(after[source], old[source] - quantity)
            self.assertEqual(after[target], old[target])
            self.assertEqual(store.transfers["TR0002" if before.transfers
                                             else "TR0001"].status,
                             "pending")
        else:
            moved = before.transfers[tid].quantity
            expected = {"dispatch": "in transit", "receive": "received",
                        "cancel": "cancelled"}[action]
            self.assertEqual(store.transfers[tid].status, expected)
            if action == "receive":
                self.assertEqual(after["NORTH"], old["NORTH"] + moved)
            if action == "cancel":
                self.assertEqual(after["MAIN"], old["MAIN"] + moved)
        self.assertTrue(all(value >= 0 for value in after.values()))
        self.assertEqual(store.products[SKU].quantity,
                         before.products[SKU].quantity)

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
                        transfer_stock(store, *args, date=TODAY)
                    self.assertEqual(store, before)
                    refused += 1
                    continue
                transfer_stock(store, *args, date=TODAY)
                self.check_success(store, before, args)
                accepted += 1
        self.assertGreater(accepted, 30)
        self.assertGreater(refused, 30)


if __name__ == "__main__":
    unittest.main()
