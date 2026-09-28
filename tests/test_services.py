import os
import tempfile
import unittest

from database import Database
from services import BudgetService, CategoryService, ExpenseService, ReportService


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.file.close()
        self.db = Database(self.file.name)
        self.db.initialize()
        self.cats = CategoryService(self.db)
        self.exps = ExpenseService(self.db)

    def tearDown(self):
        os.unlink(self.file.name)

    def category_id(self, name):
        return next(item["id"] for item in self.cats.list_categories() if item["name"] == name)

    def test_expense_crud_and_monthly_summary(self):
        cid = self.category_id("Food")
        self.exps.add_expense("125.50", "2026-09-10", cid, "Lunch")
        exp = self.exps.list_expenses("2026-09")[0]
        self.assertEqual(exp.description, "Lunch")
        self.exps.update_expense(exp.id, "150", "2026-09-11", cid, "Dinner")
        rows, total = ReportService(self.db).monthly_summary("2026-09")
        self.assertEqual(rows[0]["name"], "Food")
        self.assertEqual(total, 150)
        self.exps.delete_expense(exp.id)
        self.assertEqual(self.exps.list_expenses(), [])

    def test_budget_reports_over_budget(self):
        cid = self.category_id("Food")
        self.exps.add_expense("600", "2026-09-10", cid, "Groceries")
        BudgetService(self.db).set_budget(cid, "2026-09", "500")
        status = BudgetService(self.db).status("2026-09")[0]
        self.assertEqual(status.remaining, -100)
