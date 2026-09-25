# Smart Expense Tracker

A simple terminal-based Python application that helps a student record daily expenses, organise them by category, set category budgets, and review monthly spending. It was created as a first-year CSE project for the VITyarthi Build Your Own Project assignment.

## Features

- Add, view, edit, and delete expense records.
- Use starter categories or create simple custom categories.
- Filter expenses by month.
- View category-wise monthly spending and total spending.
- Set a monthly budget for a category and check whether it has been exceeded.
- Validate amounts, dates, month formats, empty text, and invalid record IDs.

## Technologies and tools

- Python 3.10 or later
- SQLite database through Python's built-in `sqlite3` module
- Python `unittest` for validation and service tests
- Git and GitHub for version control

No third-party package is required.

## Project structure

```text
app.py              menu and application workflow
database.py          SQLite database setup and connections
models.py            Expense and BudgetStatus data classes
services.py          category, expense, budget, and report operations
validators.py        reusable input validation
display.py           terminal table display helpers
tests/               automated tests
docs/                report source, diagrams, and screenshot placeholders
statement.md         required project statement
```

## Install and run

1. Install Python 3.10 or newer.
2. Clone the repository and open a terminal in its folder.
3. Run:

   ```bash
   python app.py
   ```

The application automatically creates `data/expense_tracker.db` and starter categories on the first run.

## Testing

Run all automated tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

The tests use a temporary database and do not change the normal application data.

## Screenshots

Real screenshots should be captured after running the application and inserted in the marked locations in [`docs/project_report.md`](docs/project_report.md). Suggested screenshots are:

- Main menu
- Adding an expense
- Monthly summary
- Budget status showing an over-budget category

## Assignment documents

- [`statement.md`](statement.md) — problem statement, scope, users, and high-level features.
- [`docs/project_report.md`](docs/project_report.md) — complete editable report source, including all required sections and diagrams.
- [`docs/requirement_checklist.md`](docs/requirement_checklist.md) — assignment requirement mapping and verification checklist.
