"""Shared test data for R9 save_data / load_data tests (Member 4)."""
import json
import os
import tempfile
import unittest

from stock_control.models import (
    AuditEntry, Batch, Category, Movement, OrderLine, Product,
    ProductSupplier, PurchaseOrder, Reservation, Supplier, Transfer, User,
    Warehouse,
)
from stock_control.reporting.storage import backup_path, save_data
from stock_control.store import Store


def make_store():
    """Store with one item in every collection. The purchase order has
    two order lines."""
    store = Store()
    store.categories["Tools"] = Category("Tools")
    store.warehouses["WH1"] = Warehouse("WH1", "Main depot")
    store.products["TLS-0001"] = Product(
        "TLS-0001", "Hammer", "Tools", 9.5, cost=5.0, quantity=12,
        min_level=5, max_level=50, stock_by_warehouse={"WH1": 12})
    store.batches.append(
        Batch("BT0001", "TLS-0001", "WH1", 12, "2026-11-01"))
    store.movements.append(
        Movement("MV0001", "TLS-0001", "receive", 12, "WH1", "2026-11-01",
                 user="clerk"))
    store.transfers["TR0001"] = Transfer("TR0001", "TLS-0001", 2, "WH1",
                                         "WH2")
    store.reservations["RS0001"] = Reservation(
        "RS0001", "TLS-0001", 1, "Bob", "2026-11-02", "2026-11-09")
    store.suppliers["SUP001"] = Supplier("SUP001", "Acme", "a@acme.co.uk",
                                         "0116 000 0000")
    store.product_suppliers.append(
        ProductSupplier("TLS-0001", "SUP001", 5.0, 3, preferred=True))
    store.purchase_orders["PO0001"] = PurchaseOrder(
        "PO0001", "SUP001",
        [OrderLine("TLS-0001", 10, 5.0), OrderLine("TLS-0001", 5, 4.5, 5)],
        created_date="2026-11-03")
    store.users["admin"] = User("admin", "salt$hash", "admin")
    store.audit_log.append(
        AuditEntry("AU0001", "admin", "update", "TLS-0001",
                   "2026-11-03T10:00", "9.0", "9.5"))
    return store


def other_store():
    """A second, different store, used as the newer version of the data."""
    store = Store()
    store.categories["Paint"] = Category("Paint")
    store.products["PNT-0001"] = Product("PNT-0001", "Paint", "Paint", 12.0)
    return store


class FileTestCase(unittest.TestCase):
    """Gives each test its own empty folder, removed after the test."""

    def setUp(self):
        self._folder = tempfile.TemporaryDirectory()
        self.folder = self._folder.name
        self.data_file = os.path.join(self.folder, "stock.json")
        self.backup_file = os.path.join(self.folder, "stock.backup.json")

    def tearDown(self):
        self._folder.cleanup()

    def write_text(self, path, text):
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def read_json(self, path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    def save_good(self, path, store):
        """Write a good saved file for store at path (no backup made)."""
        save_data(store, path)
        if os.path.exists(backup_path(path)):
            os.remove(backup_path(path))
