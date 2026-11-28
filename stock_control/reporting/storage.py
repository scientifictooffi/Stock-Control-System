import json
import os
import shutil
from dataclasses import asdict

from stock_control.models import (
    AuditEntry, Batch, Category, Movement, OrderLine, Product,
    ProductSupplier, PurchaseOrder, Reservation, Supplier, Transfer, User,
    Warehouse,
)
from stock_control.store import Store

COLLECTIONS = {
    "products": (Product, dict),
    "categories": (Category, dict),
    "warehouses": (Warehouse, dict),
    "batches": (Batch, list),
    "movements": (Movement, list),
    "transfers": (Transfer, dict),
    "reservations": (Reservation, dict),
    "suppliers": (Supplier, dict),
    "product_suppliers": (ProductSupplier, list),
    "purchase_orders": (PurchaseOrder, dict),
    "users": (User, dict),
    "audit_log": (AuditEntry, list),
}


def backup_path(file_path):
    """Name of the backup file kept next to the data file,
    e.g. data/stock.json -> data/stock.backup.json."""
    root, extension = os.path.splitext(file_path)
    return root + ".backup" + extension


def save_data(store, file_path):
    """R9 (Member 4): As an office administrator, I want the data to be
    saved with a backup so that I can recover it if a file gets damaged.

    Rules:
        1. Saved as JSON
        2. Backup made before each save
        3. Missing file starts empty
        4. Damaged file loads the backup
        5. If both fail, a clear error is shown

    save_data covers rules 1 and 2. A damaged data file is not copied
    over the backup, so a good backup is never lost.
    Returns a short message with the file name.
    Raises ValueError when store is not a Store.
    """
    if not isinstance(store, Store):
        raise ValueError("store must be a Store")
    # Rule 1: every collection as plain JSON values
    data = {}
    for name, (_, kind) in COLLECTIONS.items():
        items = getattr(store, name)
        if kind is dict:
            data[name] = {key: asdict(item) for key, item in items.items()}
        else:
            data[name] = [asdict(item) for item in items]
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    # Rule 2: copy the last good file to the backup before writing
    if _can_read(file_path):
        shutil.copyfile(file_path, backup_path(file_path))
    # Write to a temporary file first, so a save that stops half way
    # never leaves a half written data file
    temp_path = file_path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(temp_path, file_path)
    return f"data saved to {file_path}"


def load_data(file_path):
    """R9 (Member 4): As an office administrator, I want the data to be
    saved with a backup so that I can recover it if a file gets damaged.

    Rules:
        1. Saved as JSON
        2. Backup made before each save
        3. Missing file starts empty
        4. Damaged file loads the backup
        5. If both fail, a clear error is shown

    load_data covers rules 3, 4 and 5. A data file that is missing while
    its backup is still there counts as damaged.
    Returns a Store.
    Raises ValueError when neither file can be loaded.
    """
    backup = backup_path(file_path)
    # Rule 3: nothing saved yet, start with an empty store
    if not os.path.exists(file_path) and not os.path.exists(backup):
        return Store()
    try:
        return _read_store(file_path)
    except ValueError as error:
        main_problem = error
    # Rule 4: data file damaged, load the backup instead
    try:
        return _read_store(backup)
    except ValueError as error:
        # Rule 5: both files failed
        raise ValueError(
            f"could not load the data: {file_path} ({main_problem}) and "
            f"backup {backup} ({error})") from None


def _read_store(file_path):
    """Read one saved file back into a Store.
    Raises ValueError when the file is missing, is not valid JSON or does
    not match the saved layout."""
    try:
        with open(file_path, encoding="utf-8") as handle:
            data = json.load(handle)
    except OSError:
        raise ValueError("file cannot be read") from None
    except ValueError:
        raise ValueError("file is not valid JSON") from None
    if not isinstance(data, dict):
        raise ValueError("file does not hold saved data")
    store = Store()
    try:
        for name, (model, kind) in COLLECTIONS.items():
            rows = data.get(name, kind())
            if kind is dict:
                items = {key: _build(model, row) for key, row in rows.items()}
            else:
                items = [_build(model, row) for row in rows]
            setattr(store, name, items)
    except (TypeError, AttributeError):
        raise ValueError("file does not hold saved data") from None
    return store


def _can_read(file_path):
    """True when the file is there and loads without a problem."""
    try:
        _read_store(file_path)
        return True
    except ValueError:
        return False


def _build(model, row):
    """Turn one saved row back into its model. Purchase orders also hold
    their order lines."""
    item = model(**row)
    if model is PurchaseOrder:
        item.lines = [OrderLine(**line) for line in item.lines]
    return item
