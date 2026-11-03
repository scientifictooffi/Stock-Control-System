from dataclasses import dataclass, field
from typing import Dict, List

from stock_control.models import (
    AuditEntry, Batch, Category, Movement, Product, ProductSupplier,
    PurchaseOrder, Reservation, Supplier, Transfer, User, Warehouse,
)


@dataclass
class Store:
    products: Dict[str, Product] = field(default_factory=dict)
    categories: Dict[str, Category] = field(default_factory=dict)
    warehouses: Dict[str, Warehouse] = field(default_factory=dict)
    batches: List[Batch] = field(default_factory=list)
    movements: List[Movement] = field(default_factory=list)
    transfers: Dict[str, Transfer] = field(default_factory=dict)
    reservations: Dict[str, Reservation] = field(default_factory=dict)
    suppliers: Dict[str, Supplier] = field(default_factory=dict)
    product_suppliers: List[ProductSupplier] = field(default_factory=list)
    purchase_orders: Dict[str, PurchaseOrder] = field(default_factory=dict)
    users: Dict[str, User] = field(default_factory=dict)
    audit_log: List[AuditEntry] = field(default_factory=list)

    def next_id(self, prefix: str, collection) -> str:
        """Return the next sequential id such as PO0001, MV0012."""
        return f"{prefix}{len(collection) + 1:04d}"
