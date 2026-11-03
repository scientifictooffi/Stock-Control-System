from stock_control.store import Store


def save_supplier(
        store, name, email, phone, status='active', supplier_id=None):
    """S1 (Member 3): As Bee the buyer, I want to save supplier details so that
    I can contact them easily.

    Rules:
        1. Supplier name is not already used
        2. Email and phone number are valid
        3. Status is active or suspended
        4. Suspended suppliers can only be reactivated
    """
    raise NotImplementedError("S1 save_supplier is not implemented yet")


def link_product_supplier(
        store, sku, supplier_id, price, lead_time_days, preferred=False,
        pack_size=1):
    """S2 (Member 3): As Bee, I want to record which supplier sells each
    product and at what price so that I can compare them.

    Rules:
        1. Product and supplier exist and are active
        2. Price is more than 0
        3. Delivery time is 1 to 90 days
        4. Only one preferred supplier per product
    """
    raise NotImplementedError(
        "S2 link_product_supplier is not implemented yet")
