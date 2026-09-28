#this file contains important services for the project

from models import BudgetStatus, Expense
from validators import valid_amount, valid_date, valid_month, valid_text


# category service - it contains important functions like list, add, delete categories
class CategoryService:
    def __init__(self, db):
        self.db = db

    def list_categories(self):
        with self.db.connect() as con:
            return con.execute("SELECT id, name FROM categories ORDER BY name").fetchall()

    def add_category(self, name):
        name = valid_text(name, "Category name", 40)
        try:
            with self.db.connect() as con:
                con.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        except Exception as err:
            if "UNIQUE" in str(err).upper():
                raise ValueError("This category already exists.") from err
            raise

    def delete_category(self, cid):
        with self.db.connect() as con:
            used = con.execute(
                "SELECT 1 FROM expenses WHERE category_id = ?", (cid,)
            ).fetchone()
            if used:
                raise ValueError("Cannot delete a category that has expenses.")
            res = con.execute("DELETE FROM categories WHERE id = ?", (cid,))
            if res.rowcount == 0:
                raise ValueError("Category ID was not found.")


# for expense service - add, exists, list, update, delete functions.. (conatins sql query as i used sqlite as database)
class ExpenseService:
    def __init__(self, db):
        self.db = db

    def _category_exists(self, cid):
        with self.db.connect() as con:
            return con.execute("SELECT 1 FROM categories WHERE id = ?", (cid,)).fetchone()

    def add_expense(self, amount, dt, cid, text):
        amount = valid_amount(amount)
        dt = valid_date(dt)
        text = valid_text(text, "Description")
        if not self._category_exists(cid):
            raise ValueError("Category ID was not found.")
        with self.db.connect() as con:
            con.execute(
                "INSERT INTO expenses (amount, expense_date, category_id, description) VALUES (?, ?, ?, ?)",
                (amount, dt, cid, text),
            )

    def list_expenses(self, month=None, cid=None):
        sql = """
            SELECT expenses.id, expenses.amount, expenses.expense_date,
                   categories.name AS category, expenses.description
            FROM expenses JOIN categories ON expenses.category_id = categories.id
        """
        where, args = [], []
        if month:
            where.append("expenses.expense_date LIKE ?")
            args.append(valid_month(month) + "%")
        if cid:
            where.append("expenses.category_id = ?")
            args.append(cid)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY expenses.expense_date DESC, expenses.id DESC"
        with self.db.connect() as con:
            rows = con.execute(sql, args).fetchall()
        return [Expense(row["id"], row["amount"], row["expense_date"], row["category"], row["description"]) for row in rows]

    def update_expense(self, eid, amount, dt, cid, text):
        amount = valid_amount(amount)
        dt = valid_date(dt)
        text = valid_text(text, "Description")
        if not self._category_exists(cid):
            raise ValueError("Category ID was not found.")
        with self.db.connect() as con:
            res = con.execute(
                "UPDATE expenses SET amount=?, expense_date=?, category_id=?, description=? WHERE id=?",
                (amount, dt, cid, text, eid),
            )
            if res.rowcount == 0:
                raise ValueError("Expense ID was not found.")

    def delete_expense(self, eid):
        with self.db.connect() as con:
            res = con.execute("DELETE FROM expenses WHERE id = ?", (eid,))
            if res.rowcount == 0:
                raise ValueError("Expense ID was not found.")


# budgest service - set budget, status
class BudgetService:
    def __init__(self, db):
        self.db = db

    def set_budget(self, cid, month, amount):
        month, amount = valid_month(month), valid_amount(amount)
        with self.db.connect() as con:
            if not con.execute("SELECT 1 FROM categories WHERE id=?", (cid,)).fetchone():
                raise ValueError("Category ID was not found.")
            con.execute(
                "INSERT INTO budgets(category_id, month, amount) VALUES (?, ?, ?) "
                "ON CONFLICT(category_id, month) DO UPDATE SET amount=excluded.amount",
                (cid, month, amount),
            )

    def status(self, month):
        month = valid_month(month)
        sql = """
            SELECT categories.name, budgets.amount AS budget, COALESCE(SUM(expenses.amount), 0) AS spent
            FROM budgets JOIN categories ON categories.id = budgets.category_id
            LEFT JOIN expenses ON expenses.category_id = categories.id
                AND expenses.expense_date LIKE budgets.month || '%'
            WHERE budgets.month = ?
            GROUP BY budgets.id, categories.name, budgets.amount
            ORDER BY categories.name
        """
        with self.db.connect() as con:
            rows = con.execute(sql, (month,)).fetchall()
        return [BudgetStatus(row["name"], row["budget"], row["spent"]) for row in rows]


#report service - monthly summary functionality
class ReportService:
    def __init__(self, db):
        self.db = db

    def monthly_summary(self, month):
        month = valid_month(month)
        sql = """
            SELECT categories.name, COALESCE(SUM(expenses.amount), 0) AS total
            FROM expenses JOIN categories ON categories.id = expenses.category_id
            WHERE expenses.expense_date LIKE ?
            GROUP BY categories.id, categories.name
            ORDER BY total DESC, categories.name
        """
        with self.db.connect() as con:
            rows = con.execute(sql, (month + "%",)).fetchall()
        total = sum(row["total"] for row in rows)
        return rows, total
