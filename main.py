from datetime import date

from stock_control.store import Store
from stock_control.products import (
    catalogue, search, categories, levels, pricing, importer, units)
from stock_control.movements import (
    receiving, issuing, adjustments, transfers, stocktake, batches,
    reservations, returns, history)
from stock_control.purchasing import (
    suppliers, orders, approval, alerts, reorder, selection, performance)
from stock_control.purchasing import receiving as po_receiving
from stock_control.reporting import (
    auth, reports, valuation, analysis, audit, storage)

DATA_FILE = "data/stock.json"


def ask(prompt, cast=str, default=None):
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{prompt}{suffix}: ").strip()
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
    except NotImplementedError as exc:
        print("(not implemented yet:", exc, ")")
    except (ValueError, KeyError, PermissionError, FileNotFoundError) as exc:
        print("Error:", exc)


def p1_add_product(store):
    return catalogue.add_product(
        store, ask("SKU"), ask("Name"), ask("Category"), ask("Price", float),
        ask("Starting quantity", int, 0), ask("Cost", float, 0.0))


def p2_update_product(store):
    sku = ask("SKU")
    field = ask("Field (sku, name, category, price, cost)")
    kind = float if field in ("price", "cost") else str
    return catalogue.update_product(
        store, sku, {field: ask("New value", kind)})


def p3_remove_product(store):
    return catalogue.remove_product(store, ask("SKU"))


def p4_search_products(store):
    return search.search_products(store, ask("Name contains", str, ""))


def p5_manage_category(store):
    return categories.manage_category(
        store, ask("Action (add/rename/delete)"), ask("Name"),
        ask("Parent", str, "") or None)


def p6_set_stock_levels(store):
    return levels.set_stock_levels(
        store, ask("SKU"), ask("Min", int), ask("Max", int),
        ask("Reorder level", int))


def p7_calculate_price(store):
    return pricing.calculate_price(
        store, ask("SKU"), ask("Quantity", int), today())


def p8_import_products(store):
    return importer.import_products(store, ask("CSV path"))


def p9_convert_quantity(store):
    return units.convert_quantity(
        store, ask("SKU"), ask("Quantity", int),
        ask("From unit (single/box)"), ask("To unit (single/box)"))


def m1_receive_stock(store):
    return receiving.receive_stock(
        store, ask("SKU"), ask("Quantity", int), ask("Warehouse"), today(),
        ask("Use-by date YYYY-MM-DD", str, "") or None)


def m2_issue_stock(store):
    return issuing.issue_stock(
        store, ask("SKU"), ask("Quantity", int), ask("Warehouse"), today(),
        ask("Allow part order? (y/n)", str, "n").lower() == "y")


def m3_adjust_stock(store):
    return adjustments.adjust_stock(
        store, ask("SKU"), ask("Change (+/-)", int), ask("Reason"),
        ask("Warehouse"), today())


def m4_transfer_stock(store):
    return transfers.transfer_stock(
        store, ask("SKU"), ask("Quantity", int), ask("From warehouse"),
        ask("To warehouse"))


def m5_reconcile_count(store):
    return stocktake.reconcile_count(
        store, {ask("SKU"): ask("Counted", int)}, ask("Warehouse"), today())


def m6_check_expiry(store):
    return batches.check_expiry(store, today(), ask("Days", int, 30))


def m7_reserve_stock(store):
    return reservations.reserve_stock(
        store, ask("SKU"), ask("Quantity", int), ask("Customer"), today())


def m8_process_return(store):
    return returns.process_return(
        store, ask("SKU"), ask("Quantity", int), ask("Quantity bought", int),
        ask("Sale date"), today(), ask("Condition (good/damaged)"),
        ask("Warehouse"))


def m9_get_movements(store):
    return history.get_movements(store, ask("SKU", str, "") or None)


def s1_save_supplier(store):
    return suppliers.save_supplier(
        store, ask("Name"), ask("Email"), ask("Phone"))


def s2_link_product_supplier(store):
    return suppliers.link_product_supplier(
        store, ask("SKU"), ask("Supplier id"), ask("Price", float),
        ask("Lead time days", int))


def s3_create_purchase_order(store):
    return orders.create_purchase_order(
        store, ask("Supplier id"), [(ask("SKU"), ask("Quantity", int))],
        today())


def s4_approve_order(store):
    return approval.approve_order(
        store, ask("PO id"), ask("Approver username"))


def s5_receive_against_po(store):
    return po_receiving.receive_against_po(
        store, ask("PO id"), {ask("SKU"): ask("Quantity received", int)},
        ask("Warehouse"), today())


def s6_generate_alerts(store):
    return alerts.generate_alerts(store)


def s7_suggest_reorder(store):
    return reorder.suggest_reorder(
        store, ask("SKU"), ask("Average daily sales", float))


def s8_select_best_supplier(store):
    return selection.select_best_supplier(
        store, ask("SKU"), ask("Quantity", int))


def s9_rate_supplier(store):
    return performance.rate_supplier(store, ask("Supplier id"))


def r1_login(store):
    return auth.login(store, ask("Username"), ask("Password"))


def r2_check_permission(store):
    return auth.check_permission(store, ask("Username"), ask("Action"))


def r3_stock_level_report(store):
    return reports.stock_level_report(
        store, ask("Group by", str, "product"))


def r4_value_inventory(store):
    return valuation.value_inventory(
        store, ask("Method (fifo/average)", str, "fifo"))


def r5_abc_classify(store):
    return analysis.abc_classify(store, {})


def r6_turnover_ratio(store):
    return analysis.turnover_ratio(
        store, ask("SKU"), ask("Start date"), ask("End date"))


def r7_slow_moving_report(store):
    return reports.slow_moving_report(store, today())


def r8_query_audit_log(store):
    return audit.query_audit_log(store, ask("Your username"))


def r9_save_data(store):
    return storage.save_data(store, DATA_FILE)


MENU = [
    ("P1 Add product", p1_add_product),
    ("P2 Edit product", p2_update_product),
    ("P3 Remove product", p3_remove_product),
    ("P4 Search products", p4_search_products),
    ("P5 Manage category", p5_manage_category),
    ("P6 Set stock levels", p6_set_stock_levels),
    ("P7 Calculate price", p7_calculate_price),
    ("P8 Import products from CSV", p8_import_products),
    ("P9 Convert units", p9_convert_quantity),
    ("M1 Receive stock", m1_receive_stock),
    ("M2 Issue stock", m2_issue_stock),
    ("M3 Adjust stock", m3_adjust_stock),
    ("M4 Transfer stock", m4_transfer_stock),
    ("M5 Reconcile stock count", m5_reconcile_count),
    ("M6 Check expiry", m6_check_expiry),
    ("M7 Reserve stock", m7_reserve_stock),
    ("M8 Process return", m8_process_return),
    ("M9 Movement history", m9_get_movements),
    ("S1 Save supplier", s1_save_supplier),
    ("S2 Link product to supplier", s2_link_product_supplier),
    ("S3 Create purchase order", s3_create_purchase_order),
    ("S4 Approve order", s4_approve_order),
    ("S5 Receive against PO", s5_receive_against_po),
    ("S6 Low stock alerts", s6_generate_alerts),
    ("S7 Suggest reorder", s7_suggest_reorder),
    ("S8 Best supplier", s8_select_best_supplier),
    ("S9 Rate supplier", s9_rate_supplier),
    ("R1 Login", r1_login),
    ("R2 Check permission", r2_check_permission),
    ("R3 Stock level report", r3_stock_level_report),
    ("R4 Inventory value", r4_value_inventory),
    ("R5 ABC classification", r5_abc_classify),
    ("R6 Turnover ratio", r6_turnover_ratio),
    ("R7 Slow moving report", r7_slow_moving_report),
    ("R8 Audit log", r8_query_audit_log),
    ("R9 Save data", r9_save_data),
]


def load_store():
    try:
        return storage.load_data(DATA_FILE) or Store()
    except NotImplementedError:
        print("(storage not implemented yet - running in memory)")
        return Store()


def main():
    store = load_store()
    while True:
        print("\n=== Stock Control System ===")
        for number, (label, _) in enumerate(MENU, start=1):
            print(f"{number:>3}. {label}")
        print("  0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            run(lambda: storage.save_data(store, DATA_FILE))
            print("Goodbye.")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            action = MENU[int(choice) - 1][1]
            run(lambda: action(store))
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    main()
