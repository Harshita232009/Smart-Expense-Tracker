def print_categories(cats):
    if not cats:
        print("No categories found.")
        return
    print("\nID  Category")
    print("--  --------")
    for cat in cats:
        print(f"{cat['id']:<3} {cat['name']}")


def print_expenses(items):
    if not items:
        print("No expenses found.")
        return
    print("\nID  Date        Category        Amount     Description")
    print("--  ----------  --------------  ---------  ------------------------------")
    for item in items:
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
