from stock_control.storage import StockStore

PERMISSIONS = {
    "VIEWER": {"view"},
    "CLERK": {"view", "receive", "issue", "transfer"},
    "MANAGER": {"view", "receive", "issue", "transfer", "adjust", "approve_po", "price"},
    "ADMIN": {"*"},
}


def get_low_stock_alerts(store: StockStore) -> list:
    raise NotImplementedError


def calculate_stock_value(store: StockStore, method: str = "COST",
                          category: str = None) -> float:
    raise NotImplementedError


def classify_abc(store: StockStore, annual_usage: dict) -> dict:
    raise NotImplementedError


def calculate_turnover(store: StockStore, sku: str, start: str, end: str) -> dict:
    raise NotImplementedError


def generate_movement_report(store: StockStore, start: str, end: str,
                             movement_type: str = None, sku: str = None) -> dict:
    raise NotImplementedError


def forecast_demand(history: list, method: str = "SMA", periods: int = 3,
                    alpha: float = 0.3) -> float:
    raise NotImplementedError


def find_dead_stock(store: StockStore, today: str, days: int = 90) -> list:
    raise NotImplementedError


def audit_stock_records(store: StockStore) -> list:
    raise NotImplementedError


def authorise_action(role: str, action: str, amount: float = 0.0) -> bool:
    raise NotImplementedError
