# S2 link_product_supplier: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: SKU, SID (supplier id), PRICE, DAYS, PREF, PACK;
store state: PRODUCTS, SUPPLIERS, LINKS (product-supplier links).
Symbolic execution tree (one branch per decision, left = True):

  D1: SKU not in PRODUCTS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: status(SKU) != "active"
          |-T-> leaf L2: raise
          `-F-> D3: SID not in SUPPLIERS
                 |-T-> leaf L3: raise KeyError
                 `-F-> D4: status(SID) != "active"
                        |-T-> leaf L4: raise
                        `-F-> D5: PRICE not a number or bool or not finite or <= 0
                               |-T-> leaf L5: raise
                               `-F-> D6: DAYS not whole number or DAYS < 1 or DAYS > 90
                                      |-T-> leaf L6: raise
                                      `-F-> D7: PACK not whole number or PACK < 1
                                             |-T-> leaf L7: raise
                                             `-F-> D8: PREF not True/False
                                                    |-T-> leaf L8: raise
                                                    `-F-> D9: PREF & another supplier is preferred for SKU
                                                           |-T-> leaf L9: raise
                                                           `-F-> D10: link (SKU, SID) exists
                                                                  |-T-> leaf L10: update link
                                                                  `-F-> leaf L11: add new link

After L10 / L11: product.preferred_supplier = id of the preferred link or None.

Path conditions (PC) and one solution per leaf:
  L1:  SKU not in PRODUCTS                                 SKU="TAP-0001"
  L2:  SKU in PRODUCTS & status != "active"                SKU="OLD-0001"
  L3:  ... & status == "active" & SID not in SUPPLIERS     SID="SUP0009"
  L4:  ... & SID in SUPPLIERS & status(SID) != "active"    SID="SUP0003"
  L5:  ... & status(SID) == "active" & PRICE <= 0           PRICE=0
  L6:  ... & PRICE > 0 & (DAYS < 1 or DAYS > 90)           DAYS=91
  L7:  ... & 1 <= DAYS <= 90 & PACK < 1                    PACK=0
  L8:  ... & PACK >= 1 & PREF not bool                     PREF=1
  L9:  ... & PREF bool & PREF & other preferred            PREF=True, SID="SUP0002"
  L10: ... & !(PREF & other preferred) & link exists       SID="SUP0001"
  L11: ... & link does not exist                           SID="SUP0002", PREF=False
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SKU="PIP-0001", SID="SUP0002", PRICE=4.0, DAYS=7,
                    PREF=False, PACK=1   (SUP0001 is already preferred)
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D6 & !D7 & !D8 & !D9 & !D10
               -> new link (L11)
Iteration 1:  negate D10 -> link exists            => SID="SUP0001"
Iteration 2:  negate D9  -> PREF & other preferred => PREF=True, SID="SUP0002"
Iteration 3:  negate D8  -> PREF not bool          => PREF="yes"
Iteration 4:  negate D7  -> PACK < 1               => PACK=0
Iteration 5:  negate D6  -> DAYS out of 1..90      => DAYS=0
Iteration 6:  negate D5  -> PRICE <= 0             => PRICE=0
Iteration 7:  negate D4  -> status(SID) != active   => SID="SUP0003"
Iteration 8:  negate D3  -> SID not in SUPPLIERS    => SID="SUP0042"
Iteration 9:  negate D2  -> status(SKU) != active   => SKU="OLD-0001"
Iteration 10: negate D1  -> SKU not in PRODUCTS     => SKU="TAP-0001"
After iteration 10 no unexplored branch remains: 11 paths, 11 inputs.
```
