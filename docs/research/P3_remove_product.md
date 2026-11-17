# P3 remove_product: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU; store state: PRODUCTS, MOVEMENTS, ORDERS.

remove_product
  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise
   `-F-> D2: on_open_order(SKU)
          |-T-> leaf L2: raise
          `-F-> D3: PRODUCTS[SKU].quantity == 0 and not history(SKU)
                 |-T-> leaf L3: delete, return "deleted"
                 `-F-> leaf L4: status = "archived", return "archived"

_is_on_open_order(SKU)  (loop over ORDERS, unrolled once)
  D4: order.status in CLOSED        T -> skip order
  D5: any(line.sku == SKU)          T -> return True, F -> next order
  after loop -> return False

Path conditions (PC) and one solution per leaf:
  L1: SKU not in PRODUCTS                                   SKU="NOP-0000"
  L2: in PRODUCTS & exists open order with line SKU         SKU="ORD-0001"
  L3: in PRODUCTS & no open order & qty==0 & !history       SKU="NEW-0001"
  L4a: ... & no open order & qty!=0                         SKU="PIP-0001"
  L4b: ... & no open order & qty==0 & history               SKU="HIS-0001"
  L4/L3 via D4=T: order with SKU exists but status closed   SKU="DON-0001"
```

## Concolic testing

```
Iteration 0 (seed): SKU="NEW-0001" (exists, no orders, qty 0, no history)
  observed PC: !D1 & !D2 & D3 -> "deleted"
Iteration 1: negate history(SKU)=False  => SKU="HIS-0001"  -> "archived"
Iteration 2: negate quantity==0         => SKU="PIP-0001"  -> "archived"
Iteration 3: negate D5 (line.sku==SKU)  => SKU="ORD-0001"  -> raise
Iteration 4: negate D4 (status open)    => SKU="DON-0001"  -> "deleted"
Iteration 5: negate D1 (SKU in PRODUCTS)=> SKU="NOP-0000"  -> raise
After iteration 5 every branch of D1..D5 has been taken both ways.
```
