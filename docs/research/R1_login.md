# R1 login: symbolic execution and concolic testing

## Symbolic execution

```
Symbolic inputs: U (username), P (password);
store state: USERS, and for the found user: LOCKED, ACTIVE, PW, F (failed_logins).
Symbolic execution tree (one branch per decision, left = True):

  D1: U not in USERS
   |-T-> leaf L1: raise "does not exist"
   `-F-> D2: LOCKED
          |-T-> leaf L2: raise "account is locked"
          `-F-> D3: not ACTIVE
                 |-T-> leaf L3: raise "account is inactive"
                 `-F-> D4: P != PW
                        |-T-> F := F + 1
                        |     D5: F + 1 >= 3
                        |      |-T-> LOCKED := True, leaf L4: raise "now locked"
                        |      `-F-> leaf L5: raise "wrong password"
                        `-F-> F := 0, leaf L6: return user

Path conditions (PC) and one solution per leaf:
  L1: U not in USERS                                    U="nobody"
  L2: U in USERS & LOCKED                               U="kim"
  L3: U in USERS & !LOCKED & !ACTIVE                    U="lee"
  L4: ... & ACTIVE & P != PW & F + 1 >= 3               U="sam", F=2, P="wrong"
  L5: ... & ACTIVE & P != PW & F + 1 < 3                U="sam", F=0, P="wrong"
  L6: ... & ACTIVE & P == PW                            U="sam", P="pass123"

Note: D5 reads F after the update on the D4-True branch, so its symbolic
value is F + 1. Cyclomatic complexity = 5 decisions + 1 = 6 = number of leaves.
```

## Concolic testing

```
Concolic = concrete + symbolic. Start from one concrete input, record the
path condition actually followed, negate the LAST decision not yet
explored, solve for a new concrete input, repeat until every branch is covered.

Iteration 0 (seed): U="sam", P="pass123", F=0 (all rules hold)
  observed PC: !D1 & !D2 & !D3 & !D4 -> L6 success
Iteration 1: negate D4 -> P != PW                => P="wrong"     (reaches D5=F, L5)
Iteration 2: negate D5 -> F + 1 >= 3             => F=2           (L4, account locked)
Iteration 3: negate D3 -> !ACTIVE                => U="lee"       (L3)
Iteration 4: negate D2 -> LOCKED                 => U="kim"       (L2)
Iteration 5: negate D1 -> U not in USERS         => U="nobody"    (L1)
After iteration 5 no unexplored branch remains: 6 paths, 6 inputs.
```
