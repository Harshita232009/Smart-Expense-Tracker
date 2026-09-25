"""Small console-display helpers that keep the menu code readable."""


def print_categories(categories):
    if not categories:
        print("No categories found.")
        return
    print("\nID  Category")
    print("--  --------")
    for category in categories:
        print(f"{category['id']:<3} {category['name']}")


def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print("\nID  Date        Category        Amount     Description")
    print("--  ----------  --------------  ---------  ------------------------------")
    for item in expenses:
        print(f"{item.id:<3} {item.expense_date:<10}  {item.category:<14}  Rs. {item.amount:>7.2f}  {item.description}")


def print_summary(rows, total, month):
    print(f"\nExpense summary for {month}")
    print("Category        Total")
    print("--------------  ---------")
    for row in rows:
        print(f"{row['name']:<14}  Rs. {row['total']:>7.2f}")
    print(f"Total spending: Rs. {total:.2f}")


def print_budget_status(items, month):
    if not items:
        print(f"No budgets set for {month}.")
        return
    print(f"\nBudget status for {month}")
    print("Category        Budget     Spent      Remaining  Status")
    print("--------------  ---------  ---------  ---------  --------")
    for item in items:
        status = "Over budget" if item.remaining < 0 else "Within budget"
        print(f"{item.category:<14}  {item.budget:>9.2f}  {item.spent:>9.2f}  {item.remaining:>9.2f}  {status}")

