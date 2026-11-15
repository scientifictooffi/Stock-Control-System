# R2 check_permission: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: U (username), A (action);
store state: USERS, and for the found user: R (role).
Constants: ACTIONS (23 known actions), PERMS[R] (allowed actions per role).
Symbolic execution tree (one branch per decision, left = True):

  D1: U not in USERS
   |-T-> leaf L1: raise "does not exist"
   `-F-> D2: A not in ACTIONS
          |-T-> leaf L2: raise "unknown action"
          `-F-> D3: R == "admin"
                 |-T-> leaf L3: return True
                 `-F-> D4: R not in PERMS
                        |-T-> leaf L4: raise "unknown role"
                        `-F-> D5: A in PERMS[R]
                               |-T-> leaf L5: return True
                               `-F-> leaf L6: return False

Path conditions (PC) and one solution per leaf:
  L1: U not in USERS                                   U="nobody"
  L2: U in USERS & A not in ACTIONS                    U="christen", A="fly_to_moon"
  L3: U in USERS & A in ACTIONS & R="admin"            U="david", A="save_data"
  L4: ... & R!="admin" & R not in PERMS                U="ghost" (R="guest")
  L5: ... & R in PERMS & A in PERMS[R]                 U="alex", A="stocktake"
  L6: ... & R in PERMS & A not in PERMS[R]             U="christen", A="approve_order"

Note: D2 is checked before D3, so an unknown action is refused even for
an admin. Cyclomatic complexity = 5 decisions + 1 = 6 = number of leaves.
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision not yet
explored, solve for a new concrete input, repeat until every branch is covered.

Iteration 0 (seed): U="christen", A="issue_stock"
  observed PC: !D1 & !D2 & !D3 & !D4 & D5 -> L5 True
Iteration 1: negate D5 -> A not in PERMS["clerk"]   => A="change_price"  (L6 False)
Iteration 2: negate D4 -> R not in PERMS            => U="ghost"         (L4)
Iteration 3: negate D3 -> R == "admin"              => U="david"         (L3 True)
Iteration 4: negate D2 -> A not in ACTIONS          => A="fly_to_moon"   (L2)
Iteration 5: negate D1 -> U not in USERS            => U="nobody"        (L1)
After iteration 5 no unexplored branch remains: 6 paths, 6 inputs.
```
