"""Command-line entry point for the Smart Expense Tracker."""

from datetime import date

from database import Database
from display import print_budget_status, print_categories, print_expenses, print_summary
from services import BudgetService, CategoryService, ExpenseService, ReportService


class ExpenseTrackerApp:
    def __init__(self):
        database = Database()
        database.initialize()
        self.categories = CategoryService(database)
        self.expenses = ExpenseService(database)
        self.budgets = BudgetService(database)
        self.reports = ReportService(database)

    @staticmethod
    def _integer(prompt):
        try:
            return int(input(prompt))
        except ValueError as error:
            raise ValueError("Please enter a whole-number ID.") from error

    def _choose_category(self):
        print_categories(self.categories.list_categories())
        return self._integer("Category ID: ")

    def add_expense(self):
        category_id = self._choose_category()
        self.expenses.add_expense(
            input("Amount (Rs.): "), input("Date (YYYY-MM-DD): "), category_id,
            input("Description: "),
        )
        print("Expense added successfully.")

    def manage_categories(self):
        print_categories(self.categories.list_categories())
        choice = input("\n1. Add category  2. Delete category  3. Back: ").strip()
        if choice == "1":
            self.categories.add_category(input("New category name: "))
            print("Category added successfully.")
        elif choice == "2":
            self.categories.delete_category(self._integer("Category ID to delete: "))
            print("Category deleted successfully.")

    def view_expenses(self):
        month = input("Month to filter (YYYY-MM, or Enter for all): ").strip() or None
        print_expenses(self.expenses.list_expenses(month=month))

    def edit_expense(self):
        expense_id = self._integer("Expense ID to edit: ")
        category_id = self._choose_category()
        self.expenses.update_expense(
            expense_id, input("New amount (Rs.): "), input("New date (YYYY-MM-DD): "),
            category_id, input("New description: "),
        )
        print("Expense updated successfully.")

    def delete_expense(self):
        self.expenses.delete_expense(self._integer("Expense ID to delete: "))
        print("Expense deleted successfully.")

    def show_summary(self):
        month = input("Month (YYYY-MM): ").strip()
        rows, total = self.reports.monthly_summary(month)
        print_summary(rows, total, month)

    def manage_budget(self):
        month = input("Month (YYYY-MM): ").strip()
        choice = input("1. Set budget  2. View budget status: ").strip()
        if choice == "1":
            category_id = self._choose_category()
            self.budgets.set_budget(category_id, month, input("Budget amount (Rs.): "))
            print("Budget saved successfully.")
        elif choice == "2":
            print_budget_status(self.budgets.status(month), month)

    def run(self):
        actions = {
            "1": self.add_expense, "2": self.view_expenses, "3": self.edit_expense,
            "4": self.delete_expense, "5": self.manage_categories, "6": self.show_summary,
            "7": self.manage_budget,
        }
        while True:
            print("\n=== Smart Expense Tracker ===")
            print("1. Add expense\n2. View expenses\n3. Edit expense\n4. Delete expense")
            print("5. Manage categories\n6. Monthly summary\n7. Budget management\n0. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Thank you for using Smart Expense Tracker.")
                return
            action = actions.get(choice)
            if not action:
                print("Invalid option. Please choose a number from the menu.")
                continue
            try:
                action()
            except ValueError as error:
                print(f"Input error: {error}")
            except Exception as error:
                print(f"Unexpected error: {error}")


if __name__ == "__main__":
    ExpenseTrackerApp().run()

