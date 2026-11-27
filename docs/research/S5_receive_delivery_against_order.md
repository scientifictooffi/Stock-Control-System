# S5 — Receive Delivery Against Purchase Order

## User story and acceptance criteria
As Alex, I want to check a delivery against its order so that we only pay for what arrived.

- The order must have been sent.
- A partial delivery records only the quantity received.
- A full delivery closes the order.
- Up to 5% extra is accepted; more is refused.

## Interface and assumptions
The implementation preserves the supplied signature: `receive_against_po(store, po_id, received, warehouse, date, user='')`. The `received` argument is a mapping of SKU to the quantity received in the current delivery. The 5% tolerance is applied cumulatively per order line, using the integer floor of 105% of the ordered quantity. This rounding interpretation should be confirmed with the product owner for small order quantities.

A successful receipt updates the order line's received quantity, product stock, stock by warehouse, and inbound movement history. The order remains `partially_received` until all lines are fulfilled, then becomes `received`. Validation is completed before mutations are applied.

## Test design
The tests cover order status, partial and complete deliveries, the 5% tolerance, invalid quantities and SKUs, warehouse/date validation, and representative white-box paths. Symbolic and concolic files provide representative path-condition tests; they do not claim execution by a dedicated symbolic-analysis engine.
