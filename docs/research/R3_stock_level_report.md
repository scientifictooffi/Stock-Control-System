# R3 stock_level_report: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: G (group_by), C (category);
for each product: Q (quantity), MIN (min_level), MAX (max_level).
Constants: GROUP_OPTIONS = ("product", "warehouse"), CATS (store categories).
Symbolic execution tree (one branch per decision, left = True):

D1: G not in GROUP_OPTIONS
|-T-> leaf L1: raise "cannot group by"
`-F-> D2: C is not None and C not in CATS
      |-T-> leaf L2: raise "category does not exist"
      `-F-> loop over active products in C, for each line:
            S1: Q <= 0
            |-T-> leaf L3: "out"
            `-F-> S2: Q < MIN
                  |-T-> leaf L4: "low"
                  `-F-> S3: MAX > 0 and Q > MAX
                        |-T-> leaf L5: "overstocked"
                        `-F-> leaf L6: "in stock"  (MAX > 0, Q <= MAX)
                              leaf L7: "in stock"  (MAX = 0, no maximum)

Path conditions (PC) and one solution per leaf:
L1: G not in GROUP_OPTIONS                     G="supplier"
L2: G ok & C != None & C not in CATS            C="Garden"
L3: G ok & C ok & Q <= 0                         Q=0,  MIN=5, MAX=50
L4: ... & Q > 0 & Q < MIN                        Q=3,  MIN=5, MAX=50
L5: ... & Q >= MIN & MAX > 0 & Q > MAX           Q=60, MIN=5, MAX=50
L6: ... & Q >= MIN & MAX > 0 & Q <= MAX          Q=20, MIN=5, MAX=50
L7: ... & Q >= MIN & MAX = 0                     Q=60, MIN=5, MAX=0

Note: an empty store (or no product in C) skips the loop and returns [],
which is rule 4. Archived products never reach S1, so they are not in
the report.
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision not yet
explored, solve for a new concrete input, repeat until every branch is covered.

Iteration 0 (seed): G="product", C=None, Q=20, MIN=5, MAX=50
  observed PC: !D1 & !D2 & !S1 & !S2 & !S3 -> L6 "in stock"
Iteration 1: negate S3 -> MAX > 0 & Q > MAX   => Q=51       (L5 overstocked)
Iteration 2: negate S2 -> Q < MIN             => Q=4        (L4 low)
Iteration 3: negate S1 -> Q <= 0              => Q=0        (L3 out)
Iteration 4: negate D2 -> C not in CATS       => C="Garden" (L2)
Iteration 5: negate D1 -> G not in options    => G="supplier" (L1)
After iteration 5 no unexplored branch remains: 6 inputs cover every branch.
```
