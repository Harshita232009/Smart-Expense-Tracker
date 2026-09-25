import os
import tempfile
import unittest

from database import Database
from services import BudgetService, CategoryService, ExpenseService, ReportService


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.database = Database(self.temp_file.name)
        self.database.initialize()
        self.categories = CategoryService(self.database)
        self.expenses = ExpenseService(self.database)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def category_id(self, name):
        return next(item["id"] for item in self.categories.list_categories() if item["name"] == name)

    def test_expense_crud_and_monthly_summary(self):
        food_id = self.category_id("Food")
        self.expenses.add_expense("125.50", "2026-09-10", food_id, "Lunch")
        expense = self.expenses.list_expenses("2026-09")[0]
        self.assertEqual(expense.description, "Lunch")
        self.expenses.update_expense(expense.id, "150", "2026-09-11", food_id, "Dinner")
        rows, total = ReportService(self.database).monthly_summary("2026-09")
        self.assertEqual(rows[0]["name"], "Food")
        self.assertEqual(total, 150)
        self.expenses.delete_expense(expense.id)
        self.assertEqual(self.expenses.list_expenses(), [])

    def test_budget_reports_over_budget(self):
        food_id = self.category_id("Food")
        self.expenses.add_expense("600", "2026-09-10", food_id, "Groceries")
        BudgetService(self.database).set_budget(food_id, "2026-09", "500")
        status = BudgetService(self.database).status("2026-09")[0]
        self.assertEqual(status.remaining, -100)

