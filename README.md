
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

## Setup and run

Follow these steps on a new computer.

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). During installation, select **Add Python to PATH**.

Verify the installation in a terminal:

```bash
python --version
```

### 2. Clone the repository

```bash
git clone https://github.com/Harshita232009/Smart-Expense-Tracker.git
cd Smart-Expense-Tracker
```

If Git is not installed, download the repository as a ZIP file from GitHub, extract it, and open a terminal in the extracted folder.

### 3. Create and activate a virtual environment

Creating a virtual environment keeps the project dependency separate from other Python projects.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

Install the required Streamlit package:

```bash
python -m pip install -r requirements.txt
```

### 5. Configuration

No manual configuration, account, password, API key, or external database is required. On the first run, the application automatically creates a local SQLite file at `data/expense_tracker.db` and adds the starter categories: Food, Travel, Shopping, Bills, and Other.

### 6. Start the application

```bash
python -m streamlit run streamlit_app.py
```

The command opens the application in a browser, normally at `http://localhost:8501`. Use the sidebar to move between Expenses, Categories, Monthly Report, and Budgets. Press `Ctrl+C` in the terminal to stop the application.

## Testing

Run all automated tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

The tests use a temporary database and do not change the normal application data.



