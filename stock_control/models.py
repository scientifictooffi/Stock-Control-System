from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Batch:
    batch_id: str
    quantity: int
    received_date: str
    expiry_date: Optional[str] = None
    location: str = "MAIN"


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_cost: float
    selling_price: float
    reorder_level: int = 0
    status: str = "ACTIVE"
    supplier_ids: List[str] = field(default_factory=list)
    batches: List[Batch] = field(default_factory=list)
    reserved: int = 0

    @property
    def on_hand(self) -> int:
        return sum(b.quantity for b in self.batches)

    @property
    def available(self) -> int:
        return self.on_hand - self.reserved


@dataclass
class Supplier:
    supplier_id: str
    name: str
    email: str
    phone: str
    lead_time_days: int
    rating: float = 0.0
    unit_prices: dict = field(default_factory=dict)


@dataclass
class POLine:
    sku: str
    quantity: int
    unit_price: float
    received: int = 0


@dataclass
class PurchaseOrder:
    po_id: str
    supplier_id: str
    lines: List[POLine]
    status: str = "DRAFT"
    created_date: str = ""

    @property
    def total(self) -> float:
        return round(sum(l.quantity * l.unit_price for l in self.lines), 2)


@dataclass
class Movement:
    movement_id: str
    sku: str
    movement_type: str
    quantity: int
    date: str
    reference: str = ""


def to_dict(obj):
    return asdict(obj)
