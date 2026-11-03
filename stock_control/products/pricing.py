from stock_control.store import Store


def calculate_price(
        store, sku, quantity, order_date, offer_price=None, offer_start=None,
        offer_end=None):
    """P7 (Member 1): As David, the owner, I want bulk discounts worked out
    automatically so that customers who buy more pay the right price.

    Rules:
        1. 10+ items = 5% off
        2. 50+ items = 10% off
        3. Offer prices only apply between their dates
        4. Total discount never over 25%
        5. Never sell below cost
    """
    raise NotImplementedError("P7 calculate_price is not implemented yet")
