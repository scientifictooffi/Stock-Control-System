# Stock Control System — Product Backlog (Project 19)

36 user stories: 9 per member, 3 per member per sprint. Story points are **proposed** (Fibonacci). Re-estimate them in your own Planning Poker sessions and screenshot the votes for evidence.

Each story = one GitHub issue + one branch named after the story ID (for example `US-1.01-validate-sku`). Don't delete the branches after merging.

Every story maps to one function. The **Rules** in that function's docstring are the specification you test against.

| Sprint | Dates (suggested) |
|---|---|
| Sprint 1 | 27 Oct – 9 Nov 2026 |
| Sprint 2 | 10 Nov – 23 Nov 2026 |
| Sprint 3 | 24 Nov – 7 Dec 2026 |
| Hardening (report, video, coverage) | 8 Dec 2026 – 3 Jan 2027 |

## Member 1 — Product catalogue & pricing · `stock_control/product_service.py` · 34 pts

| ID | Sprint | User story | Function | SP |
|---|---|---|---|---|
| US-1.01 | 1 | As a stock clerk, I want SKUs checked for the correct format so that bad codes never enter the system. | `validate_sku` | 2 |
| US-1.02 | 1 | As a stock manager, I want to add a product with cost, price and reorder level so that it can be stocked. | `add_product` | 3 |
| US-1.03 | 1 | As a stock manager, I want to edit a product's details so that the catalogue stays accurate. | `update_product` | 5 |
| US-1.04 | 2 | As a sales assistant, I want to search products by keyword, category, price and availability so that I can answer customer queries. | `search_products` | 5 |
| US-1.05 | 2 | As a pricing manager, I want to change prices for a whole category by a percentage so that I can respond to supplier price rises. | `apply_price_change` | 3 |
| US-1.06 | 2 | As a stock manager, I want to discontinue or reactivate products safely so that obsolete lines aren't reordered. | `change_product_status` | 3 |
| US-1.07 | 3 | As a pricing manager, I want retail prices calculated from cost, markup, VAT and discount so that pricing is consistent. | `calculate_selling_price` | 3 |
| US-1.08 | 3 | As a stock manager, I want to import products from CSV lines so that I can load a supplier catalogue quickly. | `bulk_import_products` | 5 |
| US-1.09 | 3 | As a data administrator, I want likely duplicate products flagged so that the catalogue stays clean. | `find_duplicate_products` | 5 |

## Member 2 — Stock movements · `stock_control/inventory_service.py` · 34 pts

| ID | Sprint | User story | Function | SP |
|---|---|---|---|---|
| US-2.01 | 1 | As a goods-in clerk, I want to receive stock as batches with expiry dates so that stock levels and shelf life are tracked. | `receive_stock` | 3 |
| US-2.02 | 1 | As a warehouse operative, I want stock issued FIFO so that older stock leaves first and waste is reduced. | `issue_stock` | 5 |
| US-2.03 | 1 | As a stock controller, I want to adjust stock after a physical count so that records match reality. | `adjust_stock` | 5 |
| US-2.04 | 2 | As a warehouse operative, I want to transfer stock between locations so that I know where items are. | `transfer_stock` | 5 |
| US-2.05 | 2 | As a sales assistant, I want to reserve stock for an order so that it isn't sold twice. | `reserve_stock` | 3 |
| US-2.06 | 2 | As a sales assistant, I want to cancel or fulfil a reservation so that reserved stock is released correctly. | `release_reservation` | 3 |
| US-2.07 | 3 | As a returns clerk, I want returns routed by condition and age so that only sellable items go back on sale. | `process_return` | 3 |
| US-2.08 | 3 | As a stock controller, I want a list of expired and expiring batches so that I can act before stock is wasted. | `check_expiring_batches` | 3 |
| US-2.09 | 3 | As a stock controller, I want expired batches written off with their value so that losses are recorded. | `write_off_expired` | 4 |

## Member 3 — Suppliers & purchasing · `stock_control/purchasing_service.py` · 34 pts

| ID | Sprint | User story | Function | SP |
|---|---|---|---|---|
| US-3.01 | 1 | As a buyer, I want supplier emails and phone numbers validated so that we can always contact suppliers. | `validate_supplier_contact` | 2 |
| US-3.02 | 1 | As a buyer, I want to register suppliers with lead times so that orders can be planned. | `add_supplier` | 3 |
| US-3.03 | 1 | As a buyer, I want suppliers scored on delivery and quality so that I can prefer good suppliers. | `rate_supplier` | 3 |
| US-3.04 | 2 | As a buyer, I want reorder points calculated from usage, lead time and service level so that we don't run out. | `calculate_reorder_point` | 3 |
| US-3.05 | 2 | As a buyer, I want the economic order quantity calculated so that ordering and holding costs are minimised. | `calculate_eoq` | 3 |
| US-3.06 | 2 | As a buyer, I want draft purchase orders generated automatically for low-stock items so that reordering is quick. | `generate_purchase_orders` | 8 |
| US-3.07 | 3 | As a finance manager, I want POs approved within spending limits so that spending is controlled. | `approve_purchase_order` | 3 |
| US-3.08 | 3 | As a goods-in clerk, I want to receive full or partial PO deliveries so that stock and PO status update together. | `receive_purchase_order` | 5 |
| US-3.09 | 3 | As a buyer, I want the best supplier chosen by cost, rating and lead time so that orders get the best value. | `select_best_supplier` | 4 |

## Member 4 — Reporting, analytics & access control · `stock_control/report_service.py` · 34 pts

| ID | Sprint | User story | Function | SP |
|---|---|---|---|---|
| US-4.01 | 1 | As a stock manager, I want low-stock alerts by severity so that I can prioritise reordering. | `get_low_stock_alerts` | 3 |
| US-4.02 | 1 | As a finance manager, I want total stock value at cost or retail so that I can report inventory value. | `calculate_stock_value` | 3 |
| US-4.03 | 1 | As a stock manager, I want ABC classification so that I focus control on high-value items. | `classify_abc` | 5 |
| US-4.04 | 2 | As a stock manager, I want turnover and days-of-cover per product so that I can spot over-stocking. | `calculate_turnover` | 5 |
| US-4.05 | 2 | As an auditor, I want a movement report for a date range so that I can trace stock changes. | `generate_movement_report` | 3 |
| US-4.06 | 2 | As a buyer, I want demand forecasts (SMA, WMA, exponential) so that I order the right amounts. | `forecast_demand` | 5 |
| US-4.07 | 3 | As a stock manager, I want dead stock identified so that I can clear slow-moving items. | `find_dead_stock` | 3 |
| US-4.08 | 3 | As an auditor, I want the data checked for inconsistencies so that records can be trusted. | `audit_stock_records` | 4 |
| US-4.09 | 3 | As an administrator, I want actions restricted by role so that only authorised staff change stock. | `authorise_action` | 3 |

**Totals:** 136 SP. Planned velocity is about 45 SP per sprint (each member 10–13 SP per sprint).
