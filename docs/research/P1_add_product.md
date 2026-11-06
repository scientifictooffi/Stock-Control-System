# P1 add_product: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, NAME, CAT, PRICE, QTY; store state: PRODUCTS, CATS.
Symbolic execution tree (one branch per decision, left = True):

  D1: not valid(SKU)
   |-T-> leaf L1: raise
   `-F-> D2: SKU in PRODUCTS
          |-T-> leaf L2: raise
          `-F-> D3: NAME not str or strip(NAME) == ""
                 |-T-> leaf L3: raise
                 `-F-> D4: PRICE <= 0
                        |-T-> leaf L4: raise
                        `-F-> D5: QTY < 0
                               |-T-> leaf L5: raise
                               `-F-> D6: CAT not in CATS
                                      |-T-> leaf L6: raise
                                      `-F-> leaf L7: return Product

Path conditions (PC) and one solution per leaf:
  L1: !valid(SKU)                                   SKU="tap"
  L2: valid(SKU) & SKU in PRODUCTS                  SKU="PIP-0001"
  L3: valid & !in & NAME==""                        NAME=""
  L4: valid & !in & NAME!="" & PRICE<=0             PRICE=0
  L5: ... & PRICE>0 & QTY<0                         QTY=-1
  L6: ... & QTY>=0 & CAT not in CATS                CAT="Garden"
  L7: ... & CAT in CATS                             all valid
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SKU="TAP-0001", NAME="Tap", CAT="Plumbing",
                    PRICE=2.0, QTY=1 (all rules hold)
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D6 -> success
Iteration 1: negate D6 -> CAT not in CATS     => CAT="Garden"
Iteration 2: negate D5 -> QTY < 0             => QTY=-1
Iteration 3: negate D4 -> PRICE <= 0          => PRICE=0.0
Iteration 4: negate D3 -> strip(NAME) == ""   => NAME="  "
Iteration 5: negate D2 -> SKU in PRODUCTS     => SKU="PIP-0001"
Iteration 6: negate D1 -> !valid(SKU)         => SKU="PIP0001"
After iteration 6 no unexplored branch remains: 7 paths, 7 inputs.
```
