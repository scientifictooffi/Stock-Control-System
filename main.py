from datetime import date

from stock_control.storage import StockStore
from stock_control import product_service as ps
from stock_control import inventory_service as inv
from stock_control import purchasing_service as pur
from stock_control import report_service as rep


def ask(prompt, cast=str, default=None):
    raw = input(f"{prompt}{f' [{default}]' if default is not None else ''}: ").strip()
    if raw == "" and default is not None:
        return default
    return cast(raw)


def today():
    return date.today().isoformat()


def run(action):
    try:
        result = action()
        if result is not None:
            print("->", result)
    except NotImplementedError:
        print("(not implemented yet)")
    except (ValueError, KeyError, TypeError) as e:
        print("Error:", e)


def menu(store):
    options = {
        "1": ("Add product", lambda: ps.add_product(
            store, ask("SKU"), ask("Name"), ask("Category"),
            ask("Unit cost", float), ask("Selling price", float), ask("Reorder level", int, 0))),
        "2": ("Search products", lambda: ps.search_products(store, ask("Keyword", str, ""))),
        "3": ("Receive stock", lambda: inv.receive_stock(
            store, ask("SKU"), ask("Quantity", int), ask("Batch ID"), today(),
            ask("Expiry date (YYYY-MM-DD, blank for none)", str, "") or None)),
        "4": ("Issue stock", lambda: inv.issue_stock(store, ask("SKU"), ask("Quantity", int), today())),
        "5": ("Adjust stock after count", lambda: inv.adjust_stock(
            store, ask("SKU"), ask("Counted quantity", int), ask("Reason", str, "COUNT"), today())),
        "6": ("Add supplier", lambda: pur.add_supplier(
            store, ask("Name"), ask("Email"), ask("Phone"), ask("Lead time (days)", int))),
        "7": ("Generate purchase orders", lambda: pur.generate_purchase_orders(store, today())),
        "8": ("Approve purchase order", lambda: pur.approve_purchase_order(
            store, ask("PO ID"), ask("Your role (CLERK/MANAGER/DIRECTOR)"))),
        "9": ("Low-stock alerts", lambda: rep.get_low_stock_alerts(store)),
        "10": ("Stock value", lambda: rep.calculate_stock_value(store, ask("Method", str, "COST"))),
        "11": ("Expiring batches", lambda: inv.check_expiring_batches(store, today())),
        "12": ("Audit records", lambda: rep.audit_stock_records(store)),
        "0": ("Save and exit", None),
    }
    while True:
        print("\n=== Stock Control System ===")
        for key, (label, _) in options.items():
            print(f"{key:>3}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            store.save()
            print("Saved. Goodbye.")
            return
        if choice in options:
            run(options[choice][1])
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    s = StockStore()
    s.load()
    menu(s)
