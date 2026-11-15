# M3 adjust_stock: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, CHANGE, REASON, WH, APPROVER; store state: PRODUCTS,
WAREHOUSES, MANAGERS (active users with role "manager"),
STOCK = stock of SKU in WH, COST = cost price of SKU.
BIG = |CHANGE|*100 > 10*STOCK or |CHANGE|*COST > 500.
Symbolic execution tree (one branch per decision, left = True):

  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: REASON not in {damaged, lost, count error}
          |-T-> leaf L2: raise
          `-F-> D3: CHANGE not int or CHANGE is bool or CHANGE == 0
                 |-T-> leaf L3: raise
                 `-F-> D4: WH not in WAREHOUSES
                        |-T-> leaf L4: raise
                        `-F-> D5: STOCK + CHANGE < 0
                               |-T-> leaf L5: raise
                               `-F-> D6: BIG
                                      |-T-> D7: APPROVER not in MANAGERS
                                      |      |-T-> leaf L7: raise
                                      |      `-F-> leaf L8: return STOCK+CHANGE
                                      `-F-> leaf L6: return STOCK + CHANGE

Path conditions (PC) and one solution per leaf
(store: PIP-0001 STOCK=50, COST=6.0; kim is an active manager):
  L1: SKU not in PRODUCTS                            SKU="XYZ-9999"
  L2: SKU in PRODUCTS & REASON not allowed           REASON="stolen"
  L3: ... & REASON allowed & CHANGE==0               CHANGE=0
  L4: ... & CHANGE!=0 & WH not in WAREHOUSES         WH="EAST"
  L5: ... & WH in WAREHOUSES & STOCK+CHANGE<0        CHANGE=-51
  L6: ... & STOCK+CHANGE>=0 & !BIG                   CHANGE=-2
  L7: ... & BIG & APPROVER not in MANAGERS           CHANGE=-20
  L8: ... & BIG & APPROVER in MANAGERS               CHANGE=-20, APPROVER="kim"
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SKU="PIP-0001", CHANGE=-2, REASON="damaged", WH="MAIN",
                    APPROVER=None
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D6 -> success (small change)
Iteration 1: negate D6 -> BIG (2% -> 40%)        => CHANGE=-20 (D7 true)
Iteration 2: negate D7 -> APPROVER in MANAGERS   => APPROVER="kim"
Iteration 3: negate D5 -> STOCK + CHANGE < 0     => CHANGE=-60
Iteration 4: negate D4 -> WH not in WAREHOUSES   => WH="EAST"
Iteration 5: negate D3 -> CHANGE == 0            => CHANGE=0
Iteration 6: negate D2 -> REASON not allowed     => REASON="stolen"
Iteration 7: negate D1 -> SKU not in PRODUCTS    => SKU="XYZ-9999"
After iteration 7 no unexplored branch remains: 8 paths, 8 inputs.
```
