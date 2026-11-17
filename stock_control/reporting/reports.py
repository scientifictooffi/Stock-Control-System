from stock_control.store import Store


GROUP_OPTIONS = ("product", "warehouse")


def _stock_status(product, quantity):
    if quantity <= 0:
        return "out"
    if quantity < product.min_level:
        return "low"
    if product.max_level > 0 and quantity > product.max_level:
        return "overstocked"
    return "in stock"


def stock_level_report(store, group_by='product', category=None):
    """R3 (Member 4): As Alex, I want a stock report so that I can see what is
    low, out or overstocked.

    Rules:
        1. Group by product or warehouse
        2. Each line shows in stock, low, out or overstocked
        3. Can filter by category
        4. Works when there is no stock

    Details:
        - Status: "out" when the quantity is 0, "low" when it is below
          min_level, "overstocked" when it is above max_level, otherwise
          "in stock". A max_level of 0 means no maximum has been set.
        - Archived products are left out of the report.
        - Grouped by product: one line per product with its total quantity.
          Grouped by warehouse: one line per product in each warehouse.

    Returns:
        A list of lines (dicts) sorted by SKU, or by warehouse then SKU.
        An empty store gives an empty list.
    Raises ValueError for an unknown grouping or category.
    """
    if group_by not in GROUP_OPTIONS:
        raise ValueError(f"cannot group by {group_by}")
    if category is not None and category not in store.categories:
        raise ValueError(f"category {category} does not exist")
    products = [product for product in store.products.values()
                if product.status != "archived"
                and (category is None or product.category == category)]
    lines = []
    for product in sorted(products, key=lambda item: item.sku):
        if group_by == "product":
            lines.append({"sku": product.sku, "name": product.name,
                          "quantity": product.quantity,
                          "status": _stock_status(product, product.quantity)})
        else:
            for warehouse, quantity in product.stock_by_warehouse.items():
                lines.append({"warehouse": warehouse, "sku": product.sku,
                              "name": product.name, "quantity": quantity,
                              "status": _stock_status(product, quantity)})
    if group_by == "warehouse":
        lines.sort(key=lambda line: (line["warehouse"], line["sku"]))
    return lines


def slow_moving_report(store, today, days=90, slow_threshold=5):
    """R7 (Member 4): As Alex, I want a list of items that are not selling so
    that we can put them on offer.

    Rules:
        1. No sales in 90+ days = not moving
        2. Very few sales in 90 days = slow
        3. Otherwise active
        4. Limits can be changed but must be above 0
    """
    raise NotImplementedError("R7 slow_moving_report is not implemented yet")
