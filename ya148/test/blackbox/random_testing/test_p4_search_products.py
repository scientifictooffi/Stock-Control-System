import random
import string
import unittest

from stock_control.models import Category, Product
from stock_control.products.search import search_products
from stock_control.store import Store

SEED = 42
RUNS = 300
CATEGORIES = ["Plumbing", "Tools"]


def random_store(rng):
    store = Store()
    for name in CATEGORIES:
        store.categories[name] = Category(name)
    for i in range(rng.randint(0, 6)):
        name = rng.choice(["Copper pipe", "Brass tap", "Pipe cutter",
                           "Drill", "Saw", "Valve"]) + f" {i}"
        store.products[f"SKU-{i:04d}"] = Product(
            f"SKU-{i:04d}", name, rng.choice(CATEGORIES),
            round(rng.uniform(0.5, 100), 2), 1.0, rng.randint(0, 12),
            min_level=rng.randint(0, 6),
            status=rng.choice(["active", "active", "archived"]))
    return store


def random_args(rng):
    name = rng.choice(["", "pipe", "PIPE", "saw", "zzz", "p", 7])
    category = rng.choice([None, "Plumbing", "Tools", "Garden"])
    lo = rng.choice([None, -1, 0, 5, 20, 150])
    hi = rng.choice([None, -1, 0, 10, 50, 200])
    availability = rng.choice([None, "in_stock", "low", "out", "many"])
    return name, category, lo, hi, availability


def oracle(store, name, category, lo, hi, availability):
    if not isinstance(name, str):
        return "error"
    if category is not None and category not in store.categories:
        return "error"
    if (lo is not None and lo < 0) or (hi is not None and hi < 0):
        return "error"
    if lo is not None and hi is not None and lo > hi:
        return "error"
    if availability not in (None, "in_stock", "low", "out"):
        return "error"
    result = []
    for p in store.products.values():
        if p.status == "archived":
            continue
        if name.strip().lower() not in p.name.lower():
            continue
        if category is not None and p.category != category:
            continue
        if lo is not None and p.price < lo:
            continue
        if hi is not None and p.price > hi:
            continue
        state = ("out" if p.quantity <= 0
                 else "low" if p.quantity <= p.min_level else "in_stock")
        if availability is not None and state != availability:
            continue
        result.append(p.name)
    return sorted(result, key=str.lower) if result else "empty"


class TestSearchProductsRandom(unittest.TestCase):

    def test_random_searches_match_oracle(self):
        rng = random.Random(SEED)
        seen = set()
        for _ in range(RUNS):
            store = random_store(rng)
            args = random_args(rng)
            expected = oracle(store, *args)
            seen.add(expected if isinstance(expected, str) else "found")
            if expected == "error":
                with self.assertRaises(ValueError, msg=args):
                    search_products(store, *args)
            elif expected == "empty":
                with self.assertRaises(LookupError, msg=args):
                    search_products(store, *args)
            else:
                self.assertEqual(expected, [p.name for p in
                                            search_products(store, *args)])
        self.assertEqual({"error", "empty", "found"}, seen)


if __name__ == "__main__":
    unittest.main()
