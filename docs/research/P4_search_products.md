# P4 search_products: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: NAME, CAT, MIN, MAX, AVAIL; store state: PRODUCTS, CATS.

D1: NAME not str                          T -> L1 raise ValueError
D2: CAT != None and CAT not in CATS       T -> L2 raise
D3: MIN != None and MIN < 0               T -> L3 raise
D4: MAX != None and MAX < 0               T -> L4 raise
D5: MIN, MAX given and MIN > MAX          T -> L5 raise
D6: AVAIL != None and AVAIL not in SET    T -> L6 raise
loop over PRODUCTS (one unrolled iteration):
  D7:  product archived                   T -> skip
  D8:  needle and needle not in name      T -> skip
  D9:  CAT given and category != CAT      T -> skip
  D10: MIN given and price < MIN          T -> skip
  D11: MAX given and price > MAX          T -> skip
  D12: AVAIL given and state != AVAIL     T -> skip
       (state: out if qty <= 0, low if qty < min_level, else in_stock,
        same rule as R3 stock_level_report)
  all F -> append
D13: FOUND empty                          T -> L7 raise LookupError
                                          F -> L8 return sorted(FOUND)

Path conditions and one solution per leaf (store from make_store):
  L1: !str(NAME)                                   NAME=3.5
  L2: CAT given & CAT not in CATS                  CAT="Z"
  L3: MIN < 0                                      MIN=-1
  L4: MAX < 0                                      MAX=-1
  L5: MIN > MAX                                    MIN=2, MAX=1
  L6: AVAIL not in {in_stock, low, out}            AVAIL="?"
  L7: every product skipped by D7..D12             NAME="qq"
  L8: at least one product passes D7..D12          no filters
Loop decisions D7–D12 are each covered by one test that makes that
decision true for a known product and checks it is absent from the result.
```

## Concolic testing

```
Iteration 0 (seed): no filters -> observed PC: !D1..!D6 & D13=F -> 4 products
Iteration 1:  negate D13  -> NAME="zzz"            -> LookupError
Iteration 2:  negate D6   -> AVAIL="zzz"           -> ValueError
Iteration 3:  negate D5   -> MIN=5, MAX=4          -> ValueError
Iteration 4:  negate D4   -> MAX=-4                -> ValueError
Iteration 5:  negate D3   -> MIN=-4                -> ValueError
Iteration 6:  negate D2   -> CAT="zzz"             -> ValueError
Iteration 7:  negate D1   -> NAME=["pipe"]         -> ValueError
Loop branches, starting from NAME="pipe":
Iteration 8:  D8 true for Brass tap                -> 2 products
Iteration 9:  negate D9  -> CAT="Plumbing"         -> Copper pipe only
Iteration 10: negate D10 -> MIN=10                 -> Pipe cutter only
Iteration 11: negate D11 -> MAX=10                 -> Copper pipe only
Iteration 12: negate D12 -> AVAIL="out"            -> LookupError
Iteration 13: negate D7  -> OLD-0001 set active    -> Old pipe valve found
All 13 decisions have been taken both ways.
```

## Category partition

Specification: `ya148/test/blackbox/category_partition/p4_search_products.tsl`.
Four parameters, 4 error choices and 4 single choices. Frames:
4 error + 4 single + 2 x 2 x 2 x 3 = 32 frames, one test per frame in
`test_p4_search_products.py` in the same package.
