# R1 follow-up: password hashing (hash_password, hash_for_user)

Agreed at R1 Planning Poker: passwords must be hashed with a salt and
never stored in plain text. `stock_control/reporting/passwords.py` adds
this without changing `login()`: the stored value is `salt$hash`, and the
password typed at login is hashed with the same salt before `login()`
compares it.

## Symbolic execution: hash_password(P, S)

```
Symbolic inputs: P (password), S (salt).
Decisions:
  D1: P is not a str or P == ""
  D2: S is None
  D3: S is not a str or S == ""
  D4: bytes.fromhex(S) fails

  D1
   |-T-> leaf L1: raise "password must be a non-empty string"
   `-F-> D2
          |-T-> S := new random 32-digit hex  (so D3 and D4 are False)
          |      `-> leaf L2: return S + "$" + PBKDF2(P, S)
          `-F-> D3
                 |-T-> leaf L3: raise "salt must be a non-empty hex string"
                 `-F-> D4
                        |-T-> leaf L4: raise "salt must be a non-empty hex string"
                        `-F-> leaf L5: return S + "$" + PBKDF2(P, S)

Path conditions (PC) and one solution per leaf:
  L1: !(P is str & P != "")                         P=""
  L2: P is str & P != "" & S is None                P="pass123"
  L3: ... & S is not None & !(S is str & S != "")   P="pass123", S=""
  L4: ... & S is str & S != "" & S not hex          P="pass123", S="xyz"
  L5: ... & S is str & S != "" & S is hex           P="pass123", S="a1"*16

Infeasible: D2 True followed by D3 True or D4 True, because a new salt is
always a non-empty hex string. Cyclomatic complexity = 4 + 1 = 5 = leaves.
```

## Symbolic execution: hash_for_user(STORE, U, P)

```
Symbolic inputs: U (username), P (typed password);
store state: USERS, and for the found user: W (stored password).
Decisions:
  E1: U not in USERS
  E2: P is not a str or P == ""
  E3: "$" not in W
  E4: hash_password(P, salt part of W) raises ValueError

  E1
   |-T-> leaf M1: return P
   `-F-> E2
          |-T-> leaf M2: return P
          `-F-> E3
                 |-T-> leaf M3: return P
                 `-F-> E4
                        |-T-> leaf M4: return P
                        `-F-> leaf M5: return hash_password(P, salt of W)

Path conditions (PC) and one solution per leaf:
  M1: U not in USERS                                   U="nobody"
  M2: U in USERS & P == ""                             U="sam", P=""
  M3: ... & P != "" & "$" not in W                     U="old" (W="pass123")
  M4: ... & "$" in W & salt of W not hex               U="odd" (W="zz$abc")
  M5: ... & "$" in W & salt of W is hex                U="sam", P="pass123"

Cyclomatic complexity = 4 + 1 = 5 = leaves.
```

## Concolic testing: hash_password

```
Iteration 0 (seed): P="pass123", S="a1"*16
  observed PC: !D1 & !D2 & !D3 & !D4 -> L5 return
Iteration 1: negate D4 -> S not hex                  => S="xyz"     (L4)
Iteration 2: negate D3 -> S == ""                    => S=""        (L3)
Iteration 3: negate D2 -> S is None                  => S=None      (L2)
Iteration 4: negate D1 -> P == ""                    => P=""        (L1)
After iteration 4 no unexplored branch remains: 5 paths, 5 inputs.
```

## Concolic testing: hash_for_user

```
Iteration 0 (seed): U="sam", P="pass123"
  observed PC: !E1 & !E2 & !E3 & !E4 -> M5 hashed
Iteration 1: negate E4 -> salt of W not hex          => U="odd"     (M4)
Iteration 2: negate E3 -> "$" not in W               => U="old"     (M3)
Iteration 3: negate E2 -> P == ""                    => P=""        (M2)
Iteration 4: negate E1 -> U not in USERS             => U="nobody"  (M1)
After iteration 4 no unexplored branch remains: 5 paths, 5 inputs.
```
