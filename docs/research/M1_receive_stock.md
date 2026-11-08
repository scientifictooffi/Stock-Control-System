# M1 receive_stock: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, QTY, WH, DATE, USEBY; store state: PRODUCTS, WAREHOUSES.
Symbolic execution tree (one branch per decision, left = True):

  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: status(SKU) != "active"
          |-T-> leaf L2: raise
          `-F-> D3: QTY not int or QTY is bool or QTY <= 0
                 |-T-> leaf L3: raise
                 `-F-> D4: WH not in WAREHOUSES
                        |-T-> leaf L4: raise
                        `-F-> D5: not valid(DATE)
                               |-T-> leaf L5: raise
                               `-F-> D6: USEBY is None
                                      |-T-> leaf L6: return total
                                      `-F-> D7: not valid(USEBY)
                                             |-T-> leaf L7: raise
                                             `-F-> D8: USEBY < DATE
                                                    |-T-> leaf L8: raise
                                                    `-F-> leaf L9: return total

Path conditions (PC) and one solution per leaf:
  L1: SKU not in PRODUCTS                            SKU="TAP-0001"
  L2: SKU in PRODUCTS & status!="active"             SKU="OLD-0001"
  L3: ... & status=="active" & QTY<=0                QTY=0
  L4: ... & QTY>0 & WH not in WAREHOUSES             WH="EAST"
  L5: ... & WH in WAREHOUSES & !valid(DATE)          DATE="2026-02-30"
  L6: ... & valid(DATE) & USEBY==None                USEBY=None
  L7: ... & USEBY!=None & !valid(USEBY)              USEBY="2026-13-01"
  L8: ... & valid(USEBY) & USEBY<DATE                USEBY="2026-11-06"
  L9: ... & USEBY>=DATE                              USEBY="2026-11-07"
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SKU="PIP-0001", QTY=5, WH="MAIN", DATE="2026-11-07",
                    USEBY="2026-12-01" (all rules hold)
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D6 & !D7 & !D8 -> success
Iteration 1: negate D8 -> USEBY < DATE           => USEBY="2026-11-06"
Iteration 2: negate D7 -> !valid(USEBY)          => USEBY="2026-13-01"
Iteration 3: negate D6 -> USEBY is None          => USEBY=None
Iteration 4: negate D5 -> !valid(DATE)           => DATE="2026-02-30"
Iteration 5: negate D4 -> WH not in WAREHOUSES   => WH="EAST"
Iteration 6: negate D3 -> QTY <= 0               => QTY=0
Iteration 7: negate D2 -> status != "active"     => SKU="OLD-0001"
Iteration 8: negate D1 -> SKU not in PRODUCTS    => SKU="TAP-0001"
After iteration 8 no unexplored branch remains: 9 paths, 9 inputs.
```
