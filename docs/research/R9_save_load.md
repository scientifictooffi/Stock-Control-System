# R9 save_data / load_data: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: S (what is given as the store);
for the data file F and its backup B (data/stock.backup.json):
Fe, Be  = the file is there
Fok, Bok = the file loads without a problem (Fok means Fe, Bok means Be)
Constant: COLLECTIONS (the 12 collections of the store).

save_data(S, F) tree (left = True):

D1: S is not a Store
|-T-> leaf S1: raise "must be a Store"
`-F-> loop over COLLECTIONS: dict collections as {key: row},
      list collections as [row]   (D2: kind is dict, True and False)
      D3: Fok
      |-T-> leaf S2: F copied to B, then F written
      `-F-> leaf S3: F written, B not changed

load_data(F) tree:

D4: not Fe and not Be
|-T-> leaf L1: empty Store
`-F-> D5: not Fok
      |-F-> leaf L2: Store from F
      `-T-> D6: not Bok
            |-F-> leaf L3: Store from B
            `-T-> leaf L4: raise "could not load the data: F (...) and
                           backup B (...)"

_read_store(P) tree (P is F or B; this decides Fok and Bok):

D7: P cannot be opened
|-T-> leaf R1: "file cannot be read"
`-F-> D8: P is not valid JSON
      |-T-> leaf R2: "file is not valid JSON"
      `-F-> D9: top level is not an object
            |-T-> leaf R3: "file does not hold saved data"
            `-F-> loop over COLLECTIONS (D10: kind is dict),
                  each row rebuilt by _build (D12: model is PurchaseOrder,
                  then its lines are rebuilt as OrderLine)
                  D11: a row does not match its model
                  |-T-> leaf R4: "file does not hold saved data"
                  `-F-> leaf R5: Store rebuilt from P

Path conditions (PC) and one solution per leaf:
S1: S not a Store                         S = {}
S2: S Store & Fok                         F saved earlier
S3: S Store & not Fok                     F = "{x", B saved earlier
L1: not Fe & not Be                       no files
L2: (Fe or Be) & Fok                      F saved earlier
L3: (Fe or Be) & not Fok & Bok            F = "{x", B saved earlier
L4: (Fe or Be) & not Fok & not Bok        F = "{x", no B
R1: P cannot be opened                    P is a folder
R2: P opens & not JSON                    P = "{x"
R3: P opens & JSON & not an object        P = "[]"
R4: ... & object & a row does not match   P = {"products": []}
R5: ... & object & every row matches      P = "{}"

Note: L3 can also be reached with no F at all (not Fe & Be & Bok),
because a missing data file cannot be loaded either. In S3 the damaged
F is not copied over B, so a good backup is never lost.

_can_read(P) tree (used by save_data for D3):

D13: _read_store(P) raises ValueError
|-T-> leaf C1: False
`-F-> leaf C2: True

_build(M, ROW) tree (used by _read_store for every row):

D12: M is PurchaseOrder
|-T-> leaf B1: order, with its lines rebuilt as OrderLine
`-F-> leaf B2: item of model M

backup_path(P): no decisions, one path
data/stock.json -> data/stock.backup.json

C1: P missing or damaged                  P = "{x"
C2: P loads                               P saved earlier
B1: M is PurchaseOrder                    an order with one line
B2: M is not PurchaseOrder                M = Category
```

## Concolic testing

```
Start with a concrete input, run it, write down the path condition,
negate the last condition and solve it to get the next input.

load_data
It1 input: no files
    path: D4=T -> L1          PC: not Fe & not Be
    negate: Fe                -> F saved earlier
It2 input: F saved earlier
    path: D4=F D5=F -> L2     PC: Fe & Fok
    negate Fok: not Fok       -> F = "{x", no B
It3 input: F = "{x", no B
    path: D4=F D5=T D6=T -> L4   PC: Fe & not Fok & not Bok
    negate not Bok: Bok       -> B saved earlier
It4 input: F = "{x", B saved earlier
    path: D4=F D5=T D6=F -> L3   PC: Fe & not Fok & Bok

save_data
It5 input: S = None
    path: D1=T -> S1          PC: S not a Store
    negate: S is a Store      -> Store, no files
It6 input: Store, no F
    path: D1=F D3=F -> S3     PC: S Store & not Fok
    negate not Fok: Fok       -> F saved earlier
It7 input: Store, F saved earlier
    path: D1=F D3=T -> S2     PC: S Store & Fok

_read_store (data file only, no backup, so its own problem is shown)
It8 input: F is a folder
    path: D7=T -> R1          PC: cannot open
    negate: F opens           -> F = "{x" (same as It3)
    path: D7=F D8=T -> R2     PC: opens & not JSON
    negate not JSON: JSON     -> F = "[]"
It9 input: F = "[]"
    path: D9=T -> R3          PC: JSON & not an object
    negate: object            -> F = {"products": []}
It10 input: F = {"products": []}
    path: D9=F D11=T -> R4    PC: object & a row does not match
    negate: rows match        -> F = "{}"
It11 input: F = "{}"
    path: D9=F D11=F -> R5    PC: object & every row matches

_can_read and _build
It12 input: P saved earlier
    path: D13=F -> C2         PC: P loads
    negate: P does not load   -> P = "{x"
    path: D13=T -> C1         PC: not P loads
It13 input: M = Category
    path: D12=F -> B2         PC: M is not PurchaseOrder
    negate: M = PurchaseOrder -> an order with one line
    path: D12=T -> B1         PC: M is PurchaseOrder
backup_path has one path, so it is run once.

All leaves have been run and there is nothing left to negate.
The tests are in aaa192/test/whitebox/concolic_testing/test_r9_save_load.py.
```

## Category partition

Specification: `aaa192/test/blackbox/category_partition/r9_save_load.tsl`.
Two parameters and two environments, 1 error choice and 4 single choices.
Frames: 1 error + 4 single + (save_data: 3 x 2) + (load_data: 3 x 2)
= 17 frames, one test per frame in `test_r9_save_load.py` in the same
package.
