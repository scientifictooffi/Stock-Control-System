from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Category:
    name: str
    parent: Optional[str] = None


@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: float
    cost: float = 0.0
    quantity: int = 0
    min_level: int = 0
    max_level: int = 0
    reorder_level: int = 0
    box_size: int = 1
    status: str = "active"
    preferred_supplier: Optional[str] = None
    stock_by_warehouse: Dict[str, int] = field(default_factory=dict)


@dataclass
class Warehouse:
    code: str
    name: str


@dataclass
class Batch:
    batch_id: str
    sku: str
    warehouse: str
    quantity: int
    received_date: str
    use_by_date: Optional[str] = None


@dataclass
class Movement:
    movement_id: str
    sku: str
    movement_type: str
    quantity: int
    warehouse: str
    date: str
    user: str = ""
    reason: str = ""


@dataclass
class Transfer:
    transfer_id: str
    sku: str
    quantity: int
    from_warehouse: str
    to_warehouse: str
    status: str = "pending"


@dataclass
class Reservation:
    reservation_id: str
    sku: str
    quantity: int
    customer: str
    created_date: str
    expires_date: str
    status: str = "active"


@dataclass
class Supplier:
    supplier_id: str
    name: str
    email: str
    phone: str
    status: str = "active"
    min_order_value: float = 0.0
    deliveries_on_time: int = 0
    deliveries_total: int = 0
    rejected_goods: int = 0


@dataclass
class ProductSupplier:
    sku: str
    supplier_id: str
    price: float
    lead_time_days: int
    pack_size: int = 1
    preferred: bool = False


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price: float
    received: int = 0


@dataclass
class PurchaseOrder:
    po_id: str
    supplier_id: str
    lines: List[OrderLine]
    status: str = "draft"
    created_date: str = ""
    total_ex_vat: float = 0.0
    total_inc_vat: float = 0.0


@dataclass
class User:
    username: str
    password: str
    role: str
    active: bool = True
    failed_logins: int = 0
    locked: bool = False


@dataclass
class AuditEntry:
    entry_id: str
    user: str
    action: str
    entity: str
    timestamp: str
    old_value: str = ""
    new_value: str = ""
