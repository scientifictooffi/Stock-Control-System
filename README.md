# Stock Control System (CO7095 Group Project)

Backend stock control system for a small building-supplies business
(Midlands Trade Supplies case study). Python only, text menu, JSON file
storage. No GUI, no database.

Repository: https://github.com/scientifictooffi/Stock-Control-System

## 1. Requirements
- Python 3.10 or later
- PyCharm
- `coverage` package (see `requirements.txt`)

## 2. Open the project in PyCharm (Percy Gee lab)
1. Right-click the submitted `.zip` → **Extract All…** → choose a folder such as `C:\Users\<you>\Stock-Control-System`.
2. PyCharm → **File → Open** → select the extracted folder (the one that contains `main.py`) → **OK**.
3. Interpreter: **File → Settings → Project → Python Interpreter → Add Interpreter → Virtualenv → New → OK**.
4. In the PyCharm **Terminal** tab:
   ```
   pip install -r requirements.txt
   ```

## 3. Run the program
Right-click `main.py` → **Run 'main'**, or in the terminal:
```
python main.py
```
The menu lists all 36 user stories (P1–P9, M1–M9, S1–S9, R1–R9). Data is saved to `data/stock.json`.

## 4. Run the tests
Tests use the standard `unittest` module. Each member has a package
`<student_id>/test/blackbox/<technique>` and `<student_id>/test/whitebox/<technique>`.

| What | Command (run from the project root) |
|---|---|
| Everything | `python -m unittest discover -t . -s member1` (repeat for each member) |
| One technique | `python -m unittest discover -t . -s member1/test/blackbox/equivalence_partitioning` |
| Coverage for one technique | `coverage run -m unittest discover -t . -s member1/test/whitebox/branch_coverage` then `coverage report -m` |
| HTML coverage | `coverage html` → open `htmlcov/index.html` |

## 5. Project layout
```
main.py                         text menu (no business logic)
stock_control/
  models.py                     shared dataclasses
  store.py                      in-memory Store passed to every function
  products/    (Member 1)       catalogue, search, categories, levels, pricing, importer, units
  movements/   (Member 2)       receiving, issuing, adjustments, transfers, stocktake, batches, reservations, returns, history
  purchasing/  (Member 3)       suppliers, orders, approval, receiving, alerts, reorder, selection, performance
  reporting/   (Member 4)       auth, reports, valuation, analysis, audit, storage
member1/ … member4/test/        black-box and white-box test packages per member
docs/                           sprint calendar and planning evidence
data/                           stock.json is created on first save
```

## 6. Development rules
- One user story = one GitHub issue = one branch (`feature/<ID>-...`) = one pull request reviewed by another member. Branches are never deleted.
- Each function's docstring lists its **Rules**; those are the specification for all black-box tests.
- Keep logic functions pure: no `input()`/`print()` inside `stock_control/`.
- PEP 8 (PyCharm inspections must be clean before opening a PR).
- Before submission rename `member1`–`member4` to the real student user IDs.
