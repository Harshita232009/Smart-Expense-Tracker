import sqlite3
from pathlib import Path


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, typ, val, trace):
        res = super().__exit__(typ, val, trace)
        self.close()
        return res


class Database:
    def __init__(self, path="data/expense_tracker.db"):
        self.path = path

    def connect(self):
        con = sqlite3.connect(self.path, factory=ClosingConnection)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def initialize(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as con:
            con.executescript(
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
                con.execute(
                    "INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,)
                )
