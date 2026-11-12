# M2 issue_stock: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, QTY, WH, PARTIAL; store state: PRODUCTS, WAREHOUSES,
AVAIL = stock of SKU in WH, BATCHED = total of SKU's batches in WH.
ISSUE = amount that will be issued.
Symbolic execution tree (one branch per decision, left = True):

  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: QTY not int or QTY is bool or QTY <= 0
          |-T-> leaf L2: raise
          `-F-> D3: WH not in WAREHOUSES
                 |-T-> leaf L3: raise
                 `-F-> D4: QTY > AVAIL
                        |-T-> D5: not PARTIAL
                        |      |-T-> leaf L4: raise
                        |      `-F-> D6: AVAIL == 0
                        |             |-T-> leaf L5: raise
                        |             `-F-> ISSUE = AVAIL
                        |                    D9: ISSUE > BATCHED
                        |                     |-T-> leaf L9: return AVAIL
                        |                     `-F-> leaf L8: return AVAIL
                        `-F-> ISSUE = QTY
                               D9: ISSUE > BATCHED
                                |-T-> leaf L7: return QTY
                                `-F-> leaf L6: return QTY

The batch loop (D7: another batch left, D8: REMAINING == 0) takes
min(batch, REMAINING) from each batch in use-by order. It is unrolled per
batch; its result only decides D9 (whether stock outside batches is used).

Path conditions (PC) and one solution per leaf
(store: PIP-0001 AVAIL=10, BATCHED=9; TAP-0001 AVAIL=5, BATCHED=5):
  L1: SKU not in PRODUCTS                            SKU="XYZ-9999"
  L2: SKU in PRODUCTS & QTY<=0                       QTY=0
  L3: ... & QTY>0 & WH not in WAREHOUSES             WH="EAST"
  L4: ... & WH in WAREHOUSES & QTY>AVAIL & !PARTIAL  QTY=11
  L5: ... & QTY>AVAIL & PARTIAL & AVAIL==0           WH="NORTH"
  L6: ... & QTY<=AVAIL & QTY<=BATCHED                QTY=5
  L7: ... & QTY<=AVAIL & QTY>BATCHED                 QTY=10
  L8: ... & PARTIAL & AVAIL>0 & AVAIL<=BATCHED       SKU="TAP-0001", QTY=8
  L9: ... & PARTIAL & AVAIL>0 & AVAIL>BATCHED        QTY=12
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SKU="PIP-0001", QTY=5, WH="MAIN", PARTIAL=False
  observed PC: !D1 & !D2 & !D3 & !D4 & !D9 -> success (QTY<=BATCHED)
Iteration 1: negate D9 -> QTY > BATCHED          => QTY=10
Iteration 2: negate D4 -> QTY > AVAIL            => QTY=11 (D5 true)
Iteration 3: negate D5 -> PARTIAL                => PARTIAL=True
Iteration 4: negate D9 -> AVAIL <= BATCHED       => SKU="TAP-0001", QTY=8
Iteration 5: negate D6 -> AVAIL == 0             => WH="NORTH"
Iteration 6: negate D3 -> WH not in WAREHOUSES   => WH="EAST"
Iteration 7: negate D2 -> QTY <= 0               => QTY=0
Iteration 8: negate D1 -> SKU not in PRODUCTS    => SKU="XYZ-9999"
After iteration 8 no unexplored branch remains: 9 paths, 9 inputs.
```
