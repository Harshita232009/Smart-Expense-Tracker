
# Smart Expense Tracker
This is an application that I made for students to keep a record of their daily expenses, organise them by category, set category budgets, and review monthly spending. It was created as my first-year CSE project for the VITyarthi Build Your Own Project assignment. It has many features which are listed below.

## Features

- Add, view, edit, and delete expense records.
- Use starter categories or create simple custom categories.
- Filter expenses by month.
- View category-wise monthly spending and total spending.
- Set a monthly budget for a category and check whether it has been exceeded.
- Validate amounts, dates, month formats, empty text, and invalid record IDs.

## Technologies and tools

- Python 3.10 or later
- Streamlit for the browser-based user interface
- SQLite database through Python's built-in `sqlite3` module
- Python `unittest` for validation and service tests



## Project structure

```text
streamlit_app.py    Streamlit browser interface
database.py          SQLite database setup and connections
models.py            Expense and BudgetStatus data classes
services.py          category, expense, budget, and report operations
validators.py        reusable input validation
tests/               automated tests
docs/                project report
statement.md         required project statement
```

## Install and run

1. Install Python 3.10 or newer.
2. Clone the repository and open a terminal in its folder.
3. Install the one required package:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python -m streamlit run streamlit_app.py
   ```

The command opens the application in a browser. It automatically creates `data/expense_tracker.db` and starter categories on the first run.

## Testing

Run all automated tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

The tests uses a temporary database and do not change the normal application data.



