from stock_control.store import Store


def login(store, username, password):
    """R1 (Member 4): As Sam in the office, I want each staff member to log in
    with their own account so that only our staff can use the system.

    Rules:
        1. Username must exist
        2. Password is checked
        3. Account locks after 3 wrong tries
        4. Locked or inactive accounts cannot log in
    """
    raise NotImplementedError("R1 login is not implemented yet")


def check_permission(store, username, action):
    """R2 (Member 4): As David, I want each role to have its own permissions so
    that counter staff cannot change prices.

    Rules:
        1. Roles: admin, manager, clerk
        2. Each action checked against the role
        3. Unknown role or action is refused
        4. Admin can do everything
    """
    raise NotImplementedError("R2 check_permission is not implemented yet")
