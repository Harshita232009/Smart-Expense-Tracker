"""Streamlit user interface for the Smart Expense Tracker."""

from datetime import date

import streamlit as st

from database import Database
from services import BudgetService, CategoryService, ExpenseService, ReportService


@st.cache_resource
def get_services():
    """Create the database and the small service objects once per app session."""
    database = Database()
    database.initialize()
    return (
        CategoryService(database),
        ExpenseService(database),
        BudgetService(database),
        ReportService(database),
    )


def show_error(action):
    """Run an operation and display validation errors in the page."""
    try:
        action()
        st.success("Saved successfully.")
    except ValueError as error:
        st.error(str(error))


def category_options(categories):
    return {f"{item['name']} (ID: {item['id']})": item["id"] for item in categories}


def expense_page(category_service, expense_service):
    st.header("Expenses")
    categories = category_service.list_categories()
    if not categories:
        st.warning("Add a category before adding an expense.")
        return
    options = category_options(categories)

    with st.form("add_expense_form", clear_on_submit=True):
        st.subheader("Add an expense")
        amount = st.text_input("Amount (Rs.)", placeholder="Example: 125.50")
        expense_date = st.date_input("Date", value=date.today())
        selected_category = st.selectbox("Category", options)
        description = st.text_input("Description", placeholder="Example: Lunch")
        submitted = st.form_submit_button("Add expense")
    if submitted:
        show_error(lambda: expense_service.add_expense(
            amount, expense_date.isoformat(), options[selected_category], description
        ))

    st.subheader("Expense records")
    month_filter = st.text_input("Filter by month (YYYY-MM, optional)", key="expense_month")
    try:
        expenses = expense_service.list_expenses(month=month_filter or None)
    except ValueError as error:
        st.error(str(error))
        return
    if expenses:
        st.dataframe(
            [{"ID": item.id, "Date": item.expense_date, "Category": item.category,
              "Amount (Rs.)": item.amount, "Description": item.description} for item in expenses],
            hide_index=True,
            use_container_width=True,
        )
        expense_ids = {f"{item.id}: {item.description} ({item.expense_date})": item for item in expenses}
        selected_label = st.selectbox("Select an expense to edit or delete", expense_ids)
        selected = expense_ids[selected_label]
        with st.expander("Edit selected expense"):
            with st.form("edit_expense_form"):
                new_amount = st.text_input("Amount (Rs.)", value=str(selected.amount))
                new_date = st.date_input("Date", value=date.fromisoformat(selected.expense_date))
                category_names = list(options)
                index = category_names.index(next(label for label in options if label.startswith(selected.category + " (")))
                new_category = st.selectbox("Category", category_names, index=index)
                new_description = st.text_input("Description", value=selected.description)
                edit_submitted = st.form_submit_button("Update expense")
            if edit_submitted:
                show_error(lambda: expense_service.update_expense(
                    selected.id, new_amount, new_date.isoformat(), options[new_category], new_description
                ))
        if st.button("Delete selected expense", type="secondary"):
            try:
                expense_service.delete_expense(selected.id)
                st.success("Expense deleted successfully.")
            except ValueError as error:
                st.error(str(error))
    else:
        st.info("No expenses found for this filter.")


def category_page(category_service):
    st.header("Categories")
    categories = category_service.list_categories()
    st.dataframe(
        [{"ID": item["id"], "Category": item["name"]} for item in categories],
        hide_index=True,
        use_container_width=True,
    )
    with st.form("add_category_form", clear_on_submit=True):
        name = st.text_input("New category name")
        submitted = st.form_submit_button("Add category")
    if submitted:
        show_error(lambda: category_service.add_category(name))

    labels = category_options(categories)
    selected = st.selectbox("Choose an unused category to delete", labels)
    if st.button("Delete category", type="secondary"):
        try:
            category_service.delete_category(labels[selected])
            st.success("Category deleted successfully.")
        except ValueError as error:
            st.error(str(error))


def report_page(report_service):
    st.header("Monthly Report")
    month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="report_month")
    if st.button("Show monthly report"):
        try:
            rows, total = report_service.monthly_summary(month)
            st.metric("Total spending", f"Rs. {total:.2f}")
            if rows:
                st.bar_chart({row["name"]: row["total"] for row in rows})
                st.dataframe(
                    [{"Category": row["name"], "Total (Rs.)": row["total"]} for row in rows],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.info("No expenses were found for this month.")
        except ValueError as error:
            st.error(str(error))


def budget_page(category_service, budget_service):
    st.header("Monthly Budgets")
    categories = category_service.list_categories()
    options = category_options(categories)
    month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="budget_month")
    with st.form("budget_form"):
        selected_category = st.selectbox("Category", options, key="budget_category")
        amount = st.text_input("Budget amount (Rs.)")
        submitted = st.form_submit_button("Save budget")
    if submitted:
        show_error(lambda: budget_service.set_budget(options[selected_category], month, amount))

    if st.button("View budget status"):
        try:
            status = budget_service.status(month)
            if status:
                st.dataframe(
                    [{"Category": item.category, "Budget (Rs.)": item.budget,
                      "Spent (Rs.)": item.spent, "Remaining (Rs.)": item.remaining,
                      "Status": "Over budget" if item.remaining < 0 else "Within budget"}
                     for item in status],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.info("No budgets are set for this month.")
        except ValueError as error:
            st.error(str(error))


def main():
    st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")
    st.title("💰 Smart Expense Tracker")
    st.caption("A simple personal expense tracker for students.")
    category_service, expense_service, budget_service, report_service = get_services()

    pages = {
        "Expenses": lambda: expense_page(category_service, expense_service),
        "Categories": lambda: category_page(category_service),
        "Monthly Report": lambda: report_page(report_service),
        "Budgets": lambda: budget_page(category_service, budget_service),
    }
    selected_page = st.sidebar.radio("Navigate", list(pages))
    pages[selected_page]()


if __name__ == "__main__":
    main()

