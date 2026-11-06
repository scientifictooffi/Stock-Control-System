import random
import string
import unittest

from stock_control.models import Category
from stock_control.products.catalogue import add_product
from stock_control.store import Store

SEED = 42
RUNS = 200


def random_sku(rng):
    if rng.random() < 0.5:
        return (''.join(rng.choices(string.ascii_uppercase, k=3)) + "-"
                + ''.join(rng.choices(string.digits, k=4)))
    length = rng.randint(0, 10)
    return ''.join(rng.choices(string.ascii_letters + string.digits + "-",
                               k=length))


def random_name(rng):
    return rng.choice(["", "  ", "Tap", "Copper pipe", "x"])


def expected_to_fail(store, sku, name, category, price, quantity):
    import re
    if not isinstance(sku, str) or not re.match(r"^[A-Z]{3}-[0-9]{4}$", sku):
        return True
    if sku in store.products or name.strip() == "":
        return True
    if price <= 0 or quantity < 0:
        return True
    return category not in store.categories


class TestAddProductRandom(unittest.TestCase):

    def test_random_inputs_follow_the_rules(self):
        rng = random.Random(SEED)
        store = Store()
        store.categories["Plumbing"] = Category("Plumbing")
        for _ in range(RUNS):
            sku = random_sku(rng)
            name = random_name(rng)
            category = rng.choice(["Plumbing", "Garden"])
            price = round(rng.uniform(-5, 50), 2)
            quantity = rng.randint(-3, 20)
            should_fail = expected_to_fail(store, sku, name, category, price,
                                           quantity)
            if should_fail:
                with self.assertRaises(ValueError):
                    add_product(store, sku, name, category, price, quantity)
            else:
                product = add_product(store, sku, name, category, price,
                                      quantity)
                self.assertIs(product, store.products[sku])
                self.assertEqual(name.strip(), product.name)
                self.assertEqual(price, product.price)
                self.assertEqual(quantity, product.quantity)
        for product in store.products.values():
            self.assertGreater(product.price, 0)
            self.assertGreaterEqual(product.quantity, 0)
            self.assertIn(product.category, store.categories)


if __name__ == "__main__":
    unittest.main()
