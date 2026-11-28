"""R9 save_data / load_data - black-box: random testing.

30 random stores with a fixed seed, checked against the rules (oracle).
"""
import random
import unittest

from aaa192.test.r9_fixtures import FileTestCase
from stock_control.models import (
    Category, Movement, OrderLine, Product, PurchaseOrder)
from stock_control.reporting.storage import load_data, save_data
from stock_control.store import Store

SEED = 9
RUNS = 30


def random_store(rng):
    store = Store()
    store.categories["Tools"] = Category("Tools")
    for number in range(rng.randint(0, 5)):
        sku = f"TLS-{number:04d}"
        store.products[sku] = Product(
            sku, f"Item {rng.randint(1, 999)}", "Tools",
            round(rng.uniform(0.5, 100), 2),
            quantity=rng.randint(0, 200),
            stock_by_warehouse={"WH1": rng.randint(0, 50)})
        store.movements.append(Movement(
            f"MV{number:04d}", sku, rng.choice(["receive", "issue"]),
            rng.randint(1, 20), "WH1", "2026-11-01"))
    lines = [OrderLine("TLS-0000", rng.randint(1, 9), 1.5)
             for _ in range(rng.randint(0, 3))]
    store.purchase_orders["PO0001"] = PurchaseOrder("PO0001", "SUP001",
                                                    lines)
    return store


class TestSaveLoadRandom(FileTestCase):

    def test_random_round_trip(self):
        rng = random.Random(SEED)
        for run in range(RUNS):
            store = random_store(rng)
            with self.subTest(run=run):
                save_data(store, self.data_file)
                self.assertEqual(store, load_data(self.data_file))

    def test_random_backup_is_previous_save(self):
        rng = random.Random(SEED)
        for run in range(RUNS):
            first, second = random_store(rng), random_store(rng)
            with self.subTest(run=run):
                save_data(first, self.data_file)
                save_data(second, self.data_file)
                self.assertEqual(first, load_data(self.backup_file))

    def test_random_cut_file_loads_backup(self):
        rng = random.Random(SEED)
        for run in range(RUNS):
            first, second = random_store(rng), random_store(rng)
            save_data(first, self.data_file)
            save_data(second, self.data_file)
            with open(self.data_file, encoding="utf-8") as handle:
                text = handle.read()
            self.write_text(self.data_file, text[:rng.randrange(len(text))])
            with self.subTest(run=run):
                self.assertEqual(first, load_data(self.data_file))


if __name__ == "__main__":
    unittest.main()
