from stock_control.store import Store


MAX_FAILED_LOGINS = 3


def login(store, username, password):
    """R1 (Member 4): As Sam in the office, I want each staff member to log in
    with their own account so that only our staff can use the system.

    Rules:
        1. Username must exist
        2. Password is checked
        3. Account locks after 3 wrong tries
        4. Locked or inactive accounts cannot log in

    Returns the logged-in User. Raises ValueError when a rule fails.
    A wrong password adds 1 to failed_logins; on the 3rd wrong try the
    account is locked. A correct password resets failed_logins to 0.
    """
    user = store.users.get(username)
    # Rule 1: username must exist
    if user is None:
        raise ValueError(f"user {username} does not exist")
    # Rule 4: locked or inactive accounts cannot log in
    if user.locked:
        raise ValueError("account is locked")
    if not user.active:
        raise ValueError("account is inactive")
    # Rule 2: password is checked
    if user.password != password:
        user.failed_logins += 1
        # Rule 3: account locks after 3 wrong tries
        if user.failed_logins >= MAX_FAILED_LOGINS:
            user.locked = True
            raise ValueError("wrong password, account is now locked")
        raise ValueError("wrong password")
    # Success: clear the failed count and return the user
    user.failed_logins = 0
    return user


ACTIONS = {
    "search_products", "add_product", "edit_product", "remove_product",
    "change_price", "manage_category", "set_stock_levels", "import_products",
    "receive_stock", "issue_stock", "adjust_stock", "transfer_stock",
    "stocktake", "reserve_stock", "process_return", "view_history",
    "manage_suppliers", "create_order", "approve_order",
    "view_reports", "view_audit_log", "manage_users", "save_data",
}

ROLE_PERMISSIONS = {
    "manager": ACTIONS - {"manage_users"},
    "clerk": {"search_products", "issue_stock", "reserve_stock",
              "process_return", "view_reports"},
}


def check_permission(store, username, action):
    """R2 (Member 4): As David, I want each role to have its own permissions so
    that counter staff cannot change prices.

    Rules:
        1. Roles: admin, manager, clerk
        2. Each action checked against the role
        3. Unknown role or action is refused
        4. Admin can do everything

    Returns True if the user's role allows the action, False if not.
    Raises ValueError for an unknown user, action or role.
    """
    user = store.users.get(username)
    if user is None:
        raise ValueError(f"user {username} does not exist")
    if action not in ACTIONS:
        raise ValueError(f"unknown action {action}")
    if user.role == "admin":
        return True
    if user.role not in ROLE_PERMISSIONS:
        raise ValueError(f"unknown role {user.role}")
    if action in ROLE_PERMISSIONS[user.role]:
        return True
    return False
