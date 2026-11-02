from stock_control.storage import StockStore

VAT_RATES = {"STANDARD": 0.20, "REDUCED": 0.05, "ZERO": 0.0}


def validate_sku(sku: str) -> bool:
    raise NotImplementedError


def add_product(store: StockStore, sku: str, name: str, category: str,
                unit_cost: float, selling_price: float, reorder_level: int = 0):
    raise NotImplementedError


def update_product(store: StockStore, sku: str, **changes):
    raise NotImplementedError


def search_products(store: StockStore, keyword: str = "", category: str = None,
                    min_price: float = None, max_price: float = None,
                    in_stock_only: bool = False) -> list:
    raise NotImplementedError


def apply_price_change(store: StockStore, category: str, percent: float,
                       round_to: float = 0.01) -> int:
    raise NotImplementedError


def change_product_status(store: StockStore, sku: str, new_status: str) -> str:
    raise NotImplementedError


def calculate_selling_price(unit_cost: float, markup_percent: float,
                            vat_category: str = "STANDARD",
                            discount_percent: float = 0.0) -> float:
    raise NotImplementedError


def bulk_import_products(store: StockStore, csv_lines: list) -> dict:
    raise NotImplementedError


def find_duplicate_products(store: StockStore, threshold: float = 0.85) -> list:
    raise NotImplementedError
