"""Business operations for categories, expenses, budgets, and reports."""

from models import BudgetStatus, Expense
from validators import valid_amount, valid_date, valid_month, valid_text


class CategoryService:
    def __init__(self, database):
        self.database = database

    def list_categories(self):
        with self.database.connect() as connection:
            return connection.execute("SELECT id, name FROM categories ORDER BY name").fetchall()

    def add_category(self, name):
        name = valid_text(name, "Category name", 40)
        try:
            with self.database.connect() as connection:
                connection.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        except Exception as error:
            if "UNIQUE" in str(error).upper():
                raise ValueError("This category already exists.") from error
            raise

    def delete_category(self, category_id):
        with self.database.connect() as connection:
            used = connection.execute(
                "SELECT 1 FROM expenses WHERE category_id = ?", (category_id,)
            ).fetchone()
            if used:
                raise ValueError("Cannot delete a category that has expenses.")
            result = connection.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            if result.rowcount == 0:
                raise ValueError("Category ID was not found.")


class ExpenseService:
    def __init__(self, database):
        self.database = database

    def _category_exists(self, category_id):
        with self.database.connect() as connection:
            return connection.execute("SELECT 1 FROM categories WHERE id = ?", (category_id,)).fetchone()

    def add_expense(self, amount, expense_date, category_id, description):
        amount = valid_amount(amount)
        expense_date = valid_date(expense_date)
        description = valid_text(description, "Description")
        if not self._category_exists(category_id):
            raise ValueError("Category ID was not found.")
        with self.database.connect() as connection:
            connection.execute(
                "INSERT INTO expenses (amount, expense_date, category_id, description) VALUES (?, ?, ?, ?)",
                (amount, expense_date, category_id, description),
            )

    def list_expenses(self, month=None, category_id=None):
        query = """
            SELECT expenses.id, expenses.amount, expenses.expense_date,
                   categories.name AS category, expenses.description
            FROM expenses JOIN categories ON expenses.category_id = categories.id
        """
        conditions, values = [], []
        if month:
            conditions.append("expenses.expense_date LIKE ?")
            values.append(valid_month(month) + "%")
        if category_id:
            conditions.append("expenses.category_id = ?")
            values.append(category_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY expenses.expense_date DESC, expenses.id DESC"
        with self.database.connect() as connection:
            rows = connection.execute(query, values).fetchall()
        return [Expense(row["id"], row["amount"], row["expense_date"], row["category"], row["description"]) for row in rows]

    def update_expense(self, expense_id, amount, expense_date, category_id, description):
        amount = valid_amount(amount)
        expense_date = valid_date(expense_date)
        description = valid_text(description, "Description")
        if not self._category_exists(category_id):
            raise ValueError("Category ID was not found.")
        with self.database.connect() as connection:
            result = connection.execute(
                "UPDATE expenses SET amount=?, expense_date=?, category_id=?, description=? WHERE id=?",
                (amount, expense_date, category_id, description, expense_id),
            )
            if result.rowcount == 0:
                raise ValueError("Expense ID was not found.")

    def delete_expense(self, expense_id):
        with self.database.connect() as connection:
            result = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            if result.rowcount == 0:
                raise ValueError("Expense ID was not found.")


class BudgetService:
    def __init__(self, database):
        self.database = database

    def set_budget(self, category_id, month, amount):
        month, amount = valid_month(month), valid_amount(amount)
        with self.database.connect() as connection:
            if not connection.execute("SELECT 1 FROM categories WHERE id=?", (category_id,)).fetchone():
                raise ValueError("Category ID was not found.")
            connection.execute(
                "INSERT INTO budgets(category_id, month, amount) VALUES (?, ?, ?) "
                "ON CONFLICT(category_id, month) DO UPDATE SET amount=excluded.amount",
                (category_id, month, amount),
            )

    def status(self, month):
        month = valid_month(month)
        query = """
            SELECT categories.name, budgets.amount AS budget, COALESCE(SUM(expenses.amount), 0) AS spent
            FROM budgets JOIN categories ON categories.id = budgets.category_id
            LEFT JOIN expenses ON expenses.category_id = categories.id
                AND expenses.expense_date LIKE budgets.month || '%'
            WHERE budgets.month = ?
            GROUP BY budgets.id, categories.name, budgets.amount
            ORDER BY categories.name
        """
        with self.database.connect() as connection:
            rows = connection.execute(query, (month,)).fetchall()
        return [BudgetStatus(row["name"], row["budget"], row["spent"]) for row in rows]


class ReportService:
    def __init__(self, database):
        self.database = database

    def monthly_summary(self, month):
        month = valid_month(month)
        query = """
            SELECT categories.name, COALESCE(SUM(expenses.amount), 0) AS total
            FROM expenses JOIN categories ON categories.id = expenses.category_id
            WHERE expenses.expense_date LIKE ?
            GROUP BY categories.id, categories.name
            ORDER BY total DESC, categories.name
        """
        with self.database.connect() as connection:
            rows = connection.execute(query, (month + "%",)).fetchall()
        total = sum(row["total"] for row in rows)
        return rows, total

