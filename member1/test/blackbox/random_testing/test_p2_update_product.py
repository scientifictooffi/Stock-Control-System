import random
import string
import unittest

from stock_control.models import Category, Movement, Product
from stock_control.products.catalogue import update_product
from stock_control.store import Store

SEED = 42
RUNS = 300
FIELDS = ("sku", "name", "category", "price", "cost", "colour")


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.categories["Tools"] = Category("Tools")
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 4.5, 2.0, 10)
    store.products["TAP-0001"] = Product("TAP-0001", "Brass tap",
                                         "Plumbing", 12.0)
    store.products["OLD-0001"] = Product("OLD-0001", "Old valve",
                                         "Plumbing", 3.0, status="archived")
    store.movements.append(Movement("MV-1", "PIP-0001", "receipt", 10,
                                    "Main", "2026-11-03"))
    return store


def random_sku(rng):
    if rng.random() < 0.5:
        return (''.join(rng.choices(string.ascii_uppercase, k=3)) + "-"
                + ''.join(rng.choices(string.digits, k=4)))
    return rng.choice(["PIP-0001", "TAP-0001", "tap-0001", "", "TAP0001"])


def random_value(rng, field):
    if field == "sku":
        return random_sku(rng)
    if field == "name":
        return rng.choice(["", "  ", "Tap", "x", 7])
    if field == "category":
        return rng.choice(["Plumbing", "Tools", "Garden", ""])
    return round(rng.uniform(-5, 20), 2)


def random_changes(rng):
    count = rng.randint(0, 3)
    return {f: random_value(rng, f)
            for f in rng.sample(FIELDS, count)}


def expected_to_fail(store, sku, changes):
    if sku not in store.products:
        return True
    product = store.products[sku]
    if product.status == "archived" or not changes:
        return True
    for field, value in changes.items():
        if field not in ("sku", "name", "category", "price", "cost"):
            return True
        if field == "sku" and (
                any(m.sku == sku for m in store.movements)
                or not isinstance(value, str)
                or len(value) != 8 or value[3] != "-"
                or not value[:3].isupper() or not value[:3].isalpha()
                or not value[4:].isdigit() or value in store.products):
            return True
        if field == "name" and (not isinstance(value, str)
                                or value.strip() == ""):
            return True
        if field == "category" and value not in store.categories:
            return True
        if field == "price" and value <= 0:
            return True
        if field == "cost" and value < 0:
            return True
    return False


class TestUpdateProductRandom(unittest.TestCase):

    def test_random_inputs_match_oracle(self):
        rng = random.Random(SEED)
        for _ in range(RUNS):
            store = make_store()
            sku = rng.choice(["PIP-0001", "TAP-0001", "OLD-0001", "ZZZ-0000"])
            changes = random_changes(rng)
            before = {k: vars(v).copy() for k, v in store.products.items()}
            if expected_to_fail(store, sku, changes):
                with self.assertRaises(ValueError, msg=(sku, changes)):
                    update_product(store, sku, changes)
                after = {k: vars(v).copy() for k, v in store.products.items()}
                self.assertEqual(before, after, (sku, changes))
            else:
                product = update_product(store, sku, changes)
                for field, value in changes.items():
                    expected = value.strip() if field == "name" else value
                    self.assertEqual(expected, getattr(product, field))
                self.assertIs(product, store.products[product.sku])


if __name__ == "__main__":
    unittest.main()
