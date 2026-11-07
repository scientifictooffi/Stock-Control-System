# P2 update_product: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, CHANGES (map FIELD -> VALUE);
store state: PRODUCTS, CATS, MOVEMENTS.

update_product
  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise
   `-F-> D2: PRODUCTS[SKU].status == "archived"
          |-T-> leaf L2: raise
          `-F-> D3: CHANGES is empty
                 |-T-> leaf L3: raise
                 `-F-> for each (FIELD, VALUE) in CHANGES:
                        D4: FIELD not in EDITABLE_FIELDS
                         |-T-> leaf L4: raise
                         `-F-> _check_change (below)
                       after loop: apply values, rename key if FIELD "sku",
                       leaf L17: return product

_check_change(FIELD, VALUE)
  D5: FIELD == "sku"
   |-T-> D6: history(SKU)            T -> L5 raise
   |      `-F-> D7: not valid(VALUE) T -> L6 raise
   |             `-F-> D8: VALUE in PRODUCTS  T -> L7 raise, F -> L8 ok
   `-F-> D9: FIELD == "name"
          |-T-> D10: not str or strip(VALUE)==""  T -> L9 raise, F -> L10 ok
          `-F-> D11: FIELD == "category"
                 |-T-> D12: VALUE not in CATS     T -> L11 raise, F -> L12 ok
                 `-F-> D13: FIELD == "price"
                        |-T-> D14: VALUE <= 0     T -> L13 raise, F -> L14 ok
                        `-F-> (FIELD == "cost")
                               D15: VALUE < 0     T -> L15 raise, F -> L16 ok

Path conditions (PC) and one solution per leaf (one change per call):
  L1:  SKU not in PRODUCTS                          SKU="NOP-0000"
  L2:  SKU in PRODUCTS & archived                   SKU="OLD-0001"
  L3:  exists & active & CHANGES == {}              CHANGES={}
  L4:  ... & FIELD not editable                     FIELD="box_size"
  L5:  ... & FIELD="sku" & history(SKU)             SKU="PIP-0001"
  L6:  ... & FIELD="sku" & !history & !valid(VALUE) VALUE="TAP-1"
  L7:  ... & valid & VALUE in PRODUCTS              VALUE="PIP-0001"
  L8:  ... & valid & VALUE not in PRODUCTS          VALUE="TAP-0003"
  L9:  ... & FIELD="name" & strip(VALUE)==""        VALUE="\t"
  L10: ... & FIELD="name" & strip(VALUE)!=""        VALUE="N"
  L11: ... & FIELD="category" & VALUE not in CATS   VALUE="Z"
  L12: ... & FIELD="category" & VALUE in CATS       VALUE="Tools"
  L13: ... & FIELD="price" & VALUE <= 0             VALUE=-3
  L14: ... & FIELD="price" & VALUE > 0              VALUE=3
  L15: ... & FIELD="cost" & VALUE < 0               VALUE=-3
  L16: ... & FIELD="cost" & VALUE >= 0              VALUE=0
The loop is unrolled once for the tree; path 17 in the path-coverage
tests runs it twice (second change fails, first is not applied).
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record
the path condition that was followed, negate the last unexplored
decision, solve for a new concrete input, repeat.

Iteration 0 (seed): SKU="TAP-0001", CHANGES={"price": 9.0}
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D9 & !D11 & D13 & !D14
  -> success (L14)
Iteration 1:  negate D14 -> VALUE <= 0            => price 0.0      (L13)
Iteration 2:  negate D13 -> FIELD != "price"      => {"cost": 1.0}  (L16)
Iteration 3:  negate D15 -> VALUE < 0             => cost -1.0      (L15)
Iteration 4:  negate D11 -> FIELD == "category"   => "Tools"        (L12)
Iteration 5:  negate D12 -> VALUE not in CATS     => "Zoo"          (L11)
Iteration 6:  negate D9  -> FIELD == "name"       => "Tap"          (L10)
Iteration 7:  negate D10 -> strip(VALUE) == ""    => ""             (L9)
Iteration 8:  negate D5  -> FIELD == "sku"        => "TAP-0002"     (L8)
Iteration 9:  negate D8  -> VALUE in PRODUCTS     => "PIP-0001"     (L7)
Iteration 10: negate D7  -> !valid(VALUE)         => "TAP0002"      (L6)
Iteration 11: negate D6  -> history(SKU)          => SKU="PIP-0001" (L5)
Iteration 12: negate D4  -> FIELD not editable    => {"owner": "x"} (L4)
Iteration 13: negate D3  -> CHANGES empty         => {}             (L3)
Iteration 14: negate D2  -> archived              => SKU="OLD-0001" (L2)
Iteration 15: negate D1  -> SKU not in PRODUCTS   => "NOP-0000"     (L1)
After iteration 15 no unexplored branch remains: 16 leaves, 16 inputs.
```
