from stock_control.store import Store

APPROVAL_MANAGER_LIMIT = 5000.0
AUTO_APPROVAL_LIMIT = 1000.0


def approve_order(store, po_id, approver, decision='approve'):
    """S4: As a business owner, I want large purchase orders approved before
    they are sent so that I can avoid overspending.

    Orders below £1,000 are automatically approved. Orders from £1,000 up to
    and including £5,000 require a manager. Orders above £5,000 require an
    admin/owner. ``approver`` is a username stored in ``store.users``; for
    automatic orders it may be an empty string or None. A successful approval
    moves the order to ``sent`` (the in-memory system has no email transport);
    a rejection moves it to ``rejected``.
    """
    order = store.purchase_orders.get(po_id)
    if order is None:
        raise KeyError(f"purchase order {po_id} does not exist")
    if order.status not in ('draft', 'submitted'):
        raise ValueError(f"purchase order {po_id} cannot be decided from status {order.status}")
    if decision not in ('approve', 'reject'):
        raise ValueError("decision must be 'approve' or 'reject'")

    try:
        amount = float(order.total_ex_vat)
    except (TypeError, ValueError):
        raise ValueError("purchase order total must be a valid amount") from None
    if amount < 0:
        raise ValueError("purchase order total cannot be negative")

    # Validate the required approver before changing the order.
    if amount < AUTO_APPROVAL_LIMIT:
        required_role = None
    elif amount <= APPROVAL_MANAGER_LIMIT:
        required_role = 'manager'
    else:
        required_role = 'admin'

    if required_role is not None:
        user = store.users.get(approver)
        if user is None:
            raise PermissionError(f"an active {required_role} approver is required")
        if not user.active or user.locked:
            raise PermissionError("approver must be active and unlocked")
        if user.role != required_role:
            raise PermissionError(f"{required_role} approval is required")

    order.status = 'submitted'
    order.status = 'sent' if decision == 'approve' else 'rejected'
    return order
