from datetime import date

import streamlit as st

from database import Database
from services import BudgetService, CategoryService, ExpenseService, ReportService


@st.cache_resource
def get_services():
    db = Database()
    db.initialize()
    return (
        CategoryService(db),
        ExpenseService(db),
        BudgetService(db),
        ReportService(db),
    )


def show_error(action):
    try:
        action()
        st.success("Saved successfully.")
    except ValueError as err:
        st.error(str(err))


def category_options(cats):
    return {f"{item['name']} (ID: {item['id']})": item["id"] for item in cats}


def expense_page(catsvc, expsvc):
    st.header("Expenses")
    cats = catsvc.list_categories()
    if not cats:
        st.warning("Add a category before adding an expense.")
        return
    opts = category_options(cats)

    with st.form("add_expense_form", clear_on_submit=True):
        st.subheader("Add an expense")
        amount = st.text_input("Amount (Rs.)", placeholder="Example: 125.50")
        dt = st.date_input("Date", value=date.today())
        cat = st.selectbox("Category", opts)
        desc = st.text_input("Description", placeholder="Example: Lunch")
        done = st.form_submit_button("Add expense")
    if done:
        show_error(lambda: expsvc.add_expense(
            amount, dt.isoformat(), opts[cat], desc
        ))

    st.subheader("Expense records")
    month = st.text_input("Filter by month (YYYY-MM, optional)", key="expense_month")

    try:
        items = expsvc.list_expenses(month=month or None)

    except ValueError as err:
        st.error(str(err))
        return
    
    if items:
        st.dataframe(
            [{"ID": item.id, "Date": item.expense_date, "Category": item.category,
              "Amount (Rs.)": item.amount, "Description": item.description} for item in items],
            hide_index=True,
            use_container_width=True,
        )

        ids = {f"{item.id}: {item.description} ({item.expense_date})": item for item in items}
        label = st.selectbox("Select an expense to edit or delete", ids)
        item = ids[label]

        with st.expander("Edit selected expense"):
            with st.form("edit_expense_form"):
                amt = st.text_input("Amount (Rs.)", value=str(item.amount))
                dt = st.date_input("Date", value=date.fromisoformat(item.expense_date))
                names = list(opts)
                pos = names.index(next(name for name in opts if name.startswith(item.category + " (")))
                cat = st.selectbox("Category", names, index=pos)
                desc = st.text_input("Description", value=item.description)
                done = st.form_submit_button("Update expense")

            if done:
                show_error(lambda: expsvc.update_expense(
                    item.id, amt, dt.isoformat(), opts[cat], desc
                ))

        if st.button("Delete selected expense", type="secondary"):
            try:
                expsvc.delete_expense(item.id)
                st.success("Expense deleted successfully.")

            except ValueError as err:
                st.error(str(err))
    else:
        st.info("No expenses found for this filter.")


def category_page(catsvc):
    st.header("Categories")
    cats = catsvc.list_categories()
    st.dataframe(
        [{"ID": item["id"], "Category": item["name"]} for item in cats],
        hide_index=True,
        use_container_width=True,
    )

    with st.form("add_category_form", clear_on_submit=True):
        name = st.text_input("New category name")
        done = st.form_submit_button("Add category")

    if done:
        show_error(lambda: catsvc.add_category(name))

    opts = category_options(cats)
    cat = st.selectbox("Choose an unused category to delete", opts)

    if st.button("Delete category", type="secondary"):
        try:
            catsvc.delete_category(opts[cat])
            st.success("Category deleted successfully.")
        except ValueError as err:
            st.error(str(err))


def report_page(repsvc):
    st.header("Monthly Report")
    month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="report_month")

    if st.button("Show monthly report"):
        try:
            rows, total = repsvc.monthly_summary(month)
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
        except ValueError as err:
            st.error(str(err))


def budget_page(catsvc, budsvc):
    st.header("Monthly Budgets")
    cats = catsvc.list_categories()
    opts = category_options(cats)
    month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"), key="budget_month")

    with st.form("budget_form"):
        cat = st.selectbox("Category", opts, key="budget_category")
        amount = st.text_input("Budget amount (Rs.)")
        done = st.form_submit_button("Save budget")
        
    if done:
        show_error(lambda: budsvc.set_budget(opts[cat], month, amount))

    if st.button("View budget status"):
        try:
            items = budsvc.status(month)
            if items:
                st.dataframe(
                    [{"Category": item.category, "Budget (Rs.)": item.budget,
                      "Spent (Rs.)": item.spent, "Remaining (Rs.)": item.remaining,
                      "Status": "Over budget" if item.remaining < 0 else "Within budget"}
                     for item in items],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.info("No budgets are set for this month.")
        except ValueError as err:
            st.error(str(err))


def main():
    st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")
    st.title("💰 Smart Expense Tracker")
    st.caption("A simple personal expense tracker for students.")
    cats, exps, buds, reps = get_services()

    pages = {
        "Expenses": lambda: expense_page(cats, exps),
        "Categories": lambda: category_page(cats),
        "Monthly Report": lambda: report_page(reps),
        "Budgets": lambda: budget_page(cats, buds),
    }
    page = st.sidebar.radio("Navigate", list(pages))
    pages[page]()


if __name__ == "__main__":
    main()
