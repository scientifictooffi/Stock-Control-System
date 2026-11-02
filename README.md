# Stock Control System (CO7095 Group Project 19)

A backend stock control system in Python with a text menu and JSON file storage. There is no GUI and no database.

## 1. Requirements
- Python 3.10 or later
- PyCharm (Community or Professional)
- Packages: `pytest`, `pytest-cov`, `coverage`, `hypothesis` (listed in `requirements.txt`)

## 2. Uncompress and open in PyCharm (Percy Gee lab)
1. Right-click the submitted `.zip` file, choose **Extract All…**, and extract it to a folder such as `C:\Users\<you>\stock-control`.
2. Open PyCharm and choose **File → Open**. Select the extracted folder (the one containing `main.py`), then click **OK**.
3. Set the interpreter: **File → Settings → Project → Python Interpreter → Add Interpreter → Virtualenv → New**, then **OK**.
4. In the PyCharm **Terminal** tab run:
   ```
   pip install -r requirements.txt
   ```

## 3. Run the program
Right-click `main.py` and choose **Run 'main'**, or run `python main.py`. Data is saved to `data/store.json` when you choose option 0.

## 4. Run the tests
| What | Command |
|---|---|
| All tests | `pytest` |
| One member | `pytest member2` |
| One technique | `pytest member2/test/blackbox/category_partition` |
| Coverage for one technique | `pytest member2/test/whitebox/branch_coverage --cov=stock_control --cov-branch --cov-report=term-missing` |
| HTML coverage report | add `--cov-report=html`, then open `htmlcov/index.html` |

## 5. Project structure
```
Stock-Control-System/
├── main.py                       text menu
├── stock_control/
│   ├── models.py                 dataclasses
│   ├── storage.py                JSON persistence
│   ├── product_service.py        Member 1 (US-1.01 – US-1.09)
│   ├── inventory_service.py      Member 2 (US-2.01 – US-2.09)
│   ├── purchasing_service.py     Member 3 (US-3.01 – US-3.09)
│   └── report_service.py         Member 4 (US-4.01 – US-4.09)
├── member1/ … member4/test/      blackbox + whitebox test packages per member
├── data/store.json               created on first save
└── BACKLOG.md                    user stories, owners, story points
```
> Before submitting, rename `member1`–`member4` to your university user IDs as the brief requires.

## 6. GitHub
Repository: https://github.com/scientifictooffi/Stock-Control-System. Each user story has an issue and a branch named `US-x.yy-...`.
