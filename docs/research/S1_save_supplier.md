# S1 save_supplier: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: NAME, EMAIL, PHONE, STATUS, SID (supplier_id);
store state: SUPPLIERS (ids -> name, email, phone, status).
Symbolic execution tree (one branch per decision, left = True):

  D1: SID != None & SID not in SUPPLIERS
   |-T-> leaf L1: raise KeyError
   `-F-> D2: NAME not text or blank
          |-T-> leaf L2: raise
          `-F-> D3: another supplier already has NAME (ignoring letter case)
                 |-T-> leaf L3: raise
                 `-F-> D4: not valid(EMAIL)
                        |-T-> leaf L4: raise
                        `-F-> D5: not valid(PHONE)
                               |-T-> leaf L5: raise
                               `-F-> D6: STATUS not in {active, suspended}
                                      |-T-> leaf L6: raise
                                      `-F-> D7: SID == None (new supplier)
                                             |-T-> leaf L7: create supplier
                                             `-F-> D8: status(SID) == suspended
                                                    |-F-> leaf L8: update supplier
                                                    `-T-> D9: STATUS != active
                                                           |-T-> leaf L9: raise
                                                           `-F-> D10: details differ
                                                                  |-T-> leaf L10: raise
                                                                  `-F-> leaf L11: reactivate

valid(EMAIL): text, matches name@domain.tld.
valid(PHONE): text, only digits/+/space/brackets/dash, 7 to 15 digits.

Path conditions (PC) and one solution per leaf:
  L1:  SID != None & SID not in SUPPLIERS                SID="SUP0009"
  L2:  SID ok & NAME blank                               NAME="  "
  L3:  ... & NAME not blank & NAME used by other         NAME="ACME"
  L4:  ... & NAME unique & !valid(EMAIL)                 EMAIL="zed.co"
  L5:  ... & valid(EMAIL) & !valid(PHONE)                PHONE="999"
  L6:  ... & valid(PHONE) & STATUS not allowed           STATUS="dormant"
  L7:  ... & STATUS allowed & SID == None                SID=None
  L8:  ... & SID known & status(SID) != suspended        SID="SUP0001"
  L9:  ... & status(SID) == suspended & STATUS != active STATUS="suspended"
  L10: ... & STATUS == active & details differ           EMAIL="x@delta.co"
  L11: ... & details identical                           EMAIL="d@delta.co"
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision, solve for a
new concrete input, repeat until every branch has been explored.

Iteration 0 (seed): SID="SUP0002" (suspended), NAME="Delta",
                    EMAIL="d@delta.co", PHONE="01164960002", STATUS="active"
  observed PC: !D1 & !D2 & !D3 & !D4 & !D5 & !D6 & !D7 & D8 & !D9 & !D10
               -> reactivate (L11)
Iteration 1:  negate D10 -> details differ        => EMAIL="other@delta.co"
Iteration 2:  negate D9  -> STATUS != active      => STATUS="suspended"
Iteration 3:  negate D8  -> status(SID) != suspended => SID="SUP0001"
Iteration 4:  negate D7  -> SID == None           => SID=None
Iteration 5:  negate D6  -> STATUS not allowed    => STATUS="retired"
Iteration 6:  negate D5  -> !valid(PHONE)         => PHONE="12"
Iteration 7:  negate D4  -> !valid(EMAIL)         => EMAIL="zed"
Iteration 8:  negate D3  -> NAME used by other    => NAME="acme"
Iteration 9:  negate D2  -> NAME not text         => NAME=None
Iteration 10: negate D1  -> SID not in SUPPLIERS  => SID="SUP0042"
After iteration 10 no unexplored branch remains: 11 paths, 11 inputs.
```
