from stock_control.storage import StockStore

APPROVAL_LIMITS = {"CLERK": 500.0, "MANAGER": 5000.0, "DIRECTOR": float("inf")}


def validate_supplier_contact(email: str, phone: str) -> list:
    raise NotImplementedError


def add_supplier(store: StockStore, name: str, email: str, phone: str,
                 lead_time_days: int):
    raise NotImplementedError


def rate_supplier(on_time_pct: float, defect_pct: float,
                  avg_delay_days: float) -> tuple:
    raise NotImplementedError


def calculate_reorder_point(avg_daily_usage: float, lead_time_days: int,
                            safety_stock: int = 0,
                            usage_std_dev: float = None,
                            service_level: str = None) -> int:
    raise NotImplementedError


def calculate_eoq(annual_demand: float, order_cost: float,
                  holding_cost: float, min_order_qty: int = 1,
                  pack_size: int = 1) -> int:
    raise NotImplementedError


def generate_purchase_orders(store: StockStore, date: str) -> list:
    raise NotImplementedError


def approve_purchase_order(store: StockStore, po_id: str, approver_role: str) -> str:
    raise NotImplementedError


def receive_purchase_order(store: StockStore, po_id: str, received: dict,
                           date: str) -> str:
    raise NotImplementedError


def select_best_supplier(store: StockStore, sku: str, quantity: int,
                         needed_within_days: int = None) -> str:
    raise NotImplementedError
