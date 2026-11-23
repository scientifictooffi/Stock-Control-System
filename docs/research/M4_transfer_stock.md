# M4 transfer_stock: symbolic execution, concolic and condition testing

## Symbolic execution

```
Symbolic inputs: ACTION, SKU, QTY, FROM, TO, TID; store state: PRODUCTS,
WAREHOUSES, TRANSFERS, STOCK = stock of SKU in FROM,
ST = status of transfer TID, Q = quantity of transfer TID.
ALLOWED(dispatch) = {pending}, ALLOWED(receive) = {in transit},
ALLOWED(cancel) = {pending, in transit}.
Symbolic execution tree (one branch per decision, left = True):

  D1: ACTION == create
   |-T-> D2: SKU not in PRODUCTS
   |      |-T-> leaf L1: raise KeyError
   |      `-F-> D3: QTY not int or QTY is bool or QTY <= 0
   |             |-T-> leaf L2: raise
   |             `-F-> D4: FROM == TO
   |                    |-T-> leaf L3: raise
   |                    `-F-> D5: FROM not in WAREHOUSES or TO not in WAREHOUSES
   |                           |-T-> leaf L4: raise
   |                           `-F-> D6: QTY > STOCK
   |                                  |-T-> leaf L5: raise
   |                                  `-F-> leaf L6: STOCK := STOCK - QTY,
   |                                                 new transfer "pending"
   `-F-> D7: ACTION not in {dispatch, receive, cancel}
          |-T-> leaf L7: raise
          `-F-> D8: TID not in TRANSFERS
                 |-T-> leaf L8: raise KeyError
                 `-F-> D9: ST not in ALLOWED(ACTION)
                        |-T-> leaf L9: raise
                        `-F-> D10: ACTION == dispatch
                               |-T-> leaf L10: ST := in transit
                               `-F-> D11: ACTION == receive
                                      |-T-> leaf L11: ST := received,
                                      |              stock in TO += Q
                                      `-F-> leaf L12: ST := cancelled,
                                                     stock in FROM += Q

Path conditions (PC) and one solution per leaf
(store: PIP-0001 with STOCK(MAIN)=20; TR0001 = 5 units MAIN -> NORTH):
  L1:  ACTION=create & SKU not in PRODUCTS             SKU="XYZ-9999"
  L2:  ... & SKU in PRODUCTS & QTY<=0                  QTY=0
  L3:  ... & QTY>0 & FROM==TO                          FROM=TO="MAIN"
  L4:  ... & FROM!=TO & TO not in WAREHOUSES           TO="EAST"
  L5:  ... & both exist & QTY>STOCK                    QTY=21
  L6:  ... & QTY<=STOCK                                QTY=5
  L7:  ACTION!=create & ACTION not allowed             ACTION="return"
  L8:  ACTION allowed & TID not in TRANSFERS           TID="TR0001", none saved
  L9:  ... & TID in TRANSFERS & ST not in ALLOWED      cancel, ST=received
  L10: ... & ST in ALLOWED & ACTION=dispatch           ST=pending
  L11: ... & ST in ALLOWED & ACTION=receive            ST=in transit
  L12: ... & ST in ALLOWED & ACTION=cancel             ST=in transit
No loops, so the tree is finite: 12 leaves = 12 paths.
```

## Concolic testing

```
Iteration 0 (seed): ACTION=create, SKU="PIP-0001", QTY=5, FROM="MAIN",
                    TO="NORTH"
  observed PC: D1 & !D2 & !D3 & !D4 & !D5 & !D6 -> pending transfer
Iteration 1:  negate D6  -> QTY > STOCK            => QTY=25
Iteration 2:  negate D5  -> TO not in WAREHOUSES   => TO="EAST"
Iteration 3:  negate D4  -> FROM == TO             => TO="MAIN"
Iteration 4:  negate D3  -> QTY <= 0               => QTY=0
Iteration 5:  negate D2  -> SKU not in PRODUCTS    => SKU="XYZ-9999"
Iteration 6:  negate D1  -> ACTION != create       => ACTION=dispatch, TID=None
              observed PC: !D1 & !D7 & D8 -> KeyError
Iteration 7:  negate D8  -> TID in TRANSFERS       => TR0001 pending
              observed PC: ... & !D9 & D10 -> in transit
Iteration 8:  negate D10 -> ACTION != dispatch     => ACTION=cancel (L12)
Iteration 9:  negate D11 -> ACTION == receive      => ST=in transit (L11)
Iteration 10: negate D9  -> ST not in ALLOWED      => receive, ST=pending
Iteration 11: negate D7  -> ACTION not allowed     => ACTION="lose"
After iteration 11 no unexplored branch remains: 12 paths, 12 inputs.
```

## Condition testing

```
Every combination of the simple conditions inside each compound decision.

D3: C1 = QTY not int, C2 = QTY is bool, C3 = QTY <= 0
  C1 C2 C3   input   outcome
  F  F  F    5       accepted
  F  F  T    0       raise
  F  T  F    True    raise
  F  T  T    False   raise
  T  F  F    2.5     raise
  T  F  T    -1.5    raise
  T  T  -    infeasible (a bool is always an int)

D5: C4 = FROM not in WAREHOUSES, C5 = TO not in WAREHOUSES
  C4 C5   input           outcome
  F  F    MAIN -> NORTH   accepted
  F  T    MAIN -> EAST    raise
  T  F    EAST -> NORTH   raise
  T  T    EAST -> WEST    raise

D9 with D10/D11: every ACTION x ST (3 x 4 = 12). Accepted only for
  dispatch/pending, receive/in transit, cancel/pending, cancel/in transit.

Simple decisions D2, D4, D6, D7, D8 are each taken true and false.
Loop testing does not apply: transfer_stock has no loops.
```

## Category partition

Specification: `bpt5/test/blackbox/category_partition/m4_transfer_stock.tsl`.
Six parameters. The properties `Create`, `Change` and `Exists` stop impossible
mixes: product, quantity and warehouses are only chosen for create, and the
status is only chosen when a change action points at an existing transfer.
Frames: 10 error + 1 single + 1 create + 3 change actions x 4 statuses
= 23 frames, one test per frame in `test_m4_transfer_stock.py` in the same
package.
