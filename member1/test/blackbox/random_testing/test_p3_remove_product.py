import random
import unittest

from stock_control.models import (Category, Movement, OrderLine, Product,
                                  PurchaseOrder)
from stock_control.products.catalogue import remove_product
from stock_control.store import Store

SEED = 42
RUNS = 300
SKUS = ["AAA-0001", "BBB-0002", "CCC-0003"]
ORDER_STATUSES = ["draft", "sent", "approved", "received", "cancelled",
                  "closed"]


def random_store(rng):
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    for sku in SKUS:
        if rng.random() < 0.8:
            store.products[sku] = Product(sku, "Item", "Plumbing", 1.0,
                                          quantity=rng.choice([0, 0, 1, 5]))
    for i in range(rng.randint(0, 3)):
        store.movements.append(Movement(f"MV-{i}", rng.choice(SKUS),
                                        "receive", 1, "Main", "2026-11-03"))
    for i in range(rng.randint(0, 2)):
        lines = [OrderLine(rng.choice(SKUS), 1, 1.0)
                 for _ in range(rng.randint(0, 2))]
        store.purchase_orders[f"PO-{i}"] = PurchaseOrder(
            f"PO-{i}", "SUP-1", lines, rng.choice(ORDER_STATUSES))
    return store


def oracle(store, sku):
    if sku not in store.products:
        return "error"
    for order in store.purchase_orders.values():
        if order.status in ("received", "cancelled", "closed"):
            continue
        if any(line.sku == sku for line in order.lines):
            return "error"
    has_history = any(m.sku == sku for m in store.movements)
    if store.products[sku].quantity == 0 and not has_history:
        return "deleted"
    return "archived"


class TestRemoveProductRandom(unittest.TestCase):

    def test_random_stores_match_oracle(self):
        rng = random.Random(SEED)
        seen = set()
        for _ in range(RUNS):
            store = random_store(rng)
            sku = rng.choice(SKUS + ["ZZZ-9999"])
            expected = oracle(store, sku)
            seen.add(expected)
            count_before = len(store.products)
            if expected == "error":
                with self.assertRaises(ValueError, msg=sku):
                    remove_product(store, sku)
                self.assertEqual(count_before, len(store.products))
            else:
                self.assertEqual(expected, remove_product(store, sku))
                if expected == "deleted":
                    self.assertNotIn(sku, store.products)
                else:
                    self.assertEqual("archived", store.products[sku].status)
        self.assertEqual({"error", "deleted", "archived"}, seen)


if __name__ == "__main__":
    unittest.main()
