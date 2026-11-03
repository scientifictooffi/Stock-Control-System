from stock_control.store import Store


def receive_against_po(store, po_id, received, warehouse, date, user=''):
    """S5 (Member 3): As Alex, I want to check a delivery against its order so
    that we only pay for what arrived.

    Rules:
        1. Order must have been sent
        2. Part delivery = part received
        3. Full delivery closes the order
        4. Up to 5% extra is accepted, more is refused
    """
    raise NotImplementedError("S5 receive_against_po is not implemented yet")
