"""SQLite connection and table setup for the Smart Expense Tracker."""

import sqlite3
from pathlib import Path


class ClosingConnection(sqlite3.Connection):
    """A SQLite connection that closes after a ``with`` block on Windows too."""

    def __exit__(self, exc_type, exc_value, traceback):
        result = super().__exit__(exc_type, exc_value, traceback)
        self.close()
        return result


class Database:
    """Creates and supplies connections to the application's SQLite database."""

    def __init__(self, database_path="data/expense_tracker.db"):
        self.database_path = database_path

    def connect(self):
        """Return a connection whose rows can be accessed using column names."""
        connection = sqlite3.connect(self.database_path, factory=ClosingConnection)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        """Create application tables and starter categories when needed."""
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE COLLATE NOCASE
                );

                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL CHECK(amount > 0),
                    expense_date TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                );

                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    month TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    UNIQUE(category_id, month),
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                );
                """
            )
            for name in ("Food", "Travel", "Shopping", "Bills", "Other"):
                connection.execute(
                    "INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,)
                )
