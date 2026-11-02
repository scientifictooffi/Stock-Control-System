import json
import os

from stock_control.models import Product, Batch, Supplier, PurchaseOrder, POLine, Movement

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "store.json")


class StockStore:

    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.products = {}
        self.suppliers = {}
        self.purchase_orders = {}
        self.movements = []

    def save(self) -> None:
        from dataclasses import asdict
        data = {
            "products": [asdict(p) for p in self.products.values()],
            "suppliers": [asdict(s) for s in self.suppliers.values()],
            "purchase_orders": [asdict(po) for po in self.purchase_orders.values()],
            "movements": [asdict(m) for m in self.movements],
        }
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.products = {}
        for p in data.get("products", []):
            p["batches"] = [Batch(**b) for b in p.get("batches", [])]
            self.products[p["sku"]] = Product(**p)
        self.suppliers = {s["supplier_id"]: Supplier(**s) for s in data.get("suppliers", [])}
        self.purchase_orders = {}
        for po in data.get("purchase_orders", []):
            po["lines"] = [POLine(**l) for l in po["lines"]]
            self.purchase_orders[po["po_id"]] = PurchaseOrder(**po)
        self.movements = [Movement(**m) for m in data.get("movements", [])]

    def get_product(self, sku: str) -> Product:
        if sku not in self.products:
            raise KeyError(f"Unknown SKU: {sku}")
        return self.products[sku]

    def next_id(self, prefix: str, existing) -> str:
        return f"{prefix}{len(existing) + 1:04d}"
