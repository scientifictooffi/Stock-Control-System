from stock_control.store import Store


def approve_order(store, po_id, approver, decision='approve'):
    """S4 (Member 3): As David, the owner, I want large orders to be approved
    first so that we don't overspend.

    Rules:
        1. Under 1,000 pounds approved automatically
        2. 1,000 to 5,000 pounds needs Alex (manager)
        3. Over 5,000 pounds needs David (owner/admin)
        4. Order moves draft, submitted, approved or rejected, sent
    """
    raise NotImplementedError("S4 approve_order is not implemented yet")
