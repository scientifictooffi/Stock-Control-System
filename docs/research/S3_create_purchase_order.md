# S3 create_purchase_order: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SID (supplier id), LINES = [(SKU_1, QTY_1), ...], DATE;
store state: SUPPLIERS, LINKS (which supplier sells which SKU, at what price).
The loop over LINES is unrolled for 1 and 2 iterations (n = len(LINES)).
Symbolic execution tree (one branch per decision, left = True):

  D1: SID not in SUPPLIERS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: status(SID) != "active"
          |-T-> leaf L2: raise
          `-F-> D3: LINES is empty
                 |-T-> leaf L3: raise
                 `-F-> D4: not valid(DATE)
                        |-T-> leaf L4: raise
                        `-F-> iteration 1 (SEEN = {}):
                              D5: item 1 is not a (sku, qty) pair
                               |-T-> leaf L5: raise
                               `-F-> D6: SKU_1 not sold by SID
                                      |-T-> leaf L6: raise
                                      `-F-> D7: QTY_1 not whole number or <= 0
                                             |-T-> leaf L7: raise
                                             `-F-> D8: SKU_1 in SEEN
                                                    |         (infeasible: SEEN is empty)
                                                    `-F-> n == 1 ?
                                                         |-T-> D9: TOTAL_EX < MIN_ORDER(SID)
                                                         |       |-T-> leaf L8: raise
                                                         |       `-F-> leaf L9: create order
                                                         `-F-> iteration 2 (SEEN = {SKU_1}):
                                                               D5: item 2 is not a pair
                                                                |-T-> leaf L10: raise
                                                                `-F-> D6: SKU_2 not sold by SID
                                                                       |-T-> leaf L11: raise
                                                                       `-F-> D7: QTY_2 invalid
                                                                              |-T-> leaf L12: raise
                                                                              `-F-> D8: SKU_2 == SKU_1
                                                                                     |-T-> leaf L13: raise
                                                                                     `-F-> D9: TOTAL_EX < MIN_ORDER(SID)
                                                                                            |-T-> leaf L14: raise
                                                                                            `-F-> leaf L15: create order

TOTAL_EX = sum(QTY_i x price(SID, SKU_i)), rounded to the penny.
TOTAL_INC = TOTAL_EX x 1.20, rounded to the penny (halves up).
Further iterations repeat the iteration-2 pattern (loop is bounded by LINES).

Path conditions (PC) and one solution per leaf (SUP0001: minimum order 50,
sells PIP-0001 at 10 and TAP-0002 at 5; SUP0002 is suspended):
  L1:  SID not in SUPPLIERS                              SID="SUP0009"
  L2:  SID in SUPPLIERS & status != "active"             SID="SUP0002"
  L3:  ... & active & LINES == []                        LINES=[]
  L4:  ... & LINES != [] & !valid(DATE)                  DATE="2026-02-30"
  L5:  ... & valid(DATE) & item 1 not a pair             LINES=["PIP-0001"]
  L6:  ... & item 1 a pair & SKU_1 not sold by SID       SKU_1="BRK-0003"
  L7:  ... & SKU_1 sold & QTY_1 <= 0                     QTY_1=0
  L8:  ... & QTY_1 > 0 & n == 1 & TOTAL_EX < 50          LINES=[("PIP-0001",4)]
  L9:  ... & n == 1 & TOTAL_EX >= 50                     LINES=[("PIP-0001",5)]
  L10: ... & n >= 2 & item 2 not a pair                  item 2 = "TAP-0002"
  L11: ... & item 2 a pair & SKU_2 not sold by SID       SKU_2="BRK-0003"
  L12: ... & SKU_2 sold & QTY_2 <= 0                     QTY_2=-1
  L13: ... & QTY_2 > 0 & SKU_2 == SKU_1                  SKU_2="PIP-0001"
  L14: ... & SKU_2 != SKU_1 & TOTAL_EX < 50              [("PIP-0001",1),("TAP-0002",1)]
  L15: ... & TOTAL_EX >= 50                              [("PIP-0001",6),("TAP-0002",2)]
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.
Decisions D5-D8 happen once per item, so they are written D5.1 (item 1) and
D5.2 (item 2).

Iteration 0 (seed): SID="SUP0001", LINES=[("PIP-0001",6),("TAP-0002",2)],
                    DATE="2026-11-07"  (TOTAL_EX = 70, all rules hold)
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5.1 & !D6.1 & !D7.1 & !D8.1
               & !D5.2 & !D6.2 & !D7.2 & !D8.2 & !D9 -> order created
Iteration 1:  negate D9    -> TOTAL_EX < 50          => [("PIP-0001",1),("TAP-0002",1)]
Iteration 2:  negate D8.2  -> SKU_2 == SKU_1         => [("PIP-0001",6),("PIP-0001",2)]
Iteration 3:  negate D7.2  -> QTY_2 <= 0             => QTY_2=0
Iteration 4:  negate D6.2  -> SKU_2 not sold by SID  => SKU_2="BRK-0003"
Iteration 5:  negate D5.2  -> item 2 not a pair      => item 2 = "TAP-0002"
Iteration 6:  negate D7.1  -> QTY_1 <= 0             => QTY_1=0
Iteration 7:  negate D6.1  -> SKU_1 not sold by SID  => SKU_1="BRK-0003"
Iteration 8:  negate D5.1  -> item 1 not a pair      => item 1 = None
Iteration 9:  negate D4    -> !valid(DATE)           => DATE="07-11-2026"
Iteration 10: negate D3    -> LINES is empty         => LINES=[]
Iteration 11: negate D2    -> status(SID) != active  => SID="SUP0002"
Iteration 12: negate D1    -> SID not in SUPPLIERS   => SID="SUP0042"
Negating D8.1 (SKU_1 in SEEN) is unsatisfiable because SEEN is still empty
during the first iteration, so the solver finds no input and no test is
written for it.
After iteration 12 no feasible unexplored branch remains: 13 concrete inputs
(1 order created, 12 refused). The one-item success path (n = 1) is covered
in the symbolic execution tests (leaf L9).
```
