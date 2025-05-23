import streamlit as st
import csv
import os
from datetime import datetime, timedelta
from expense import Expense
import pandas as pd

CSV_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"
DEFAULT_BUDGET = 2000.0  # Use float for consistency

def load_budget():
    if os.path.isfile(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            try:
                return float(f.read())
            except:
                return DEFAULT_BUDGET
    else:
        return DEFAULT_BUDGET

def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(budget))

# Initialize budget from persistent storage
if "budget" not in st.session_state:
    st.session_state["budget"] = load_budget()

st.title("💸 Expense Tracker")

# Sidebar for budget
st.sidebar.header("Set Your Monthly Budget")
new_budget = st.sidebar.number_input(
    "Monthly Budget ($)",
    min_value=0.0,
    value=float(st.session_state["budget"]),
    step=10.0
)
if new_budget != st.session_state["budget"]:
    st.session_state["budget"] = new_budget
    save_budget(new_budget)
    st.sidebar.success(f"Budget set to ${new_budget:.2f}")

# Ensure CSV exists
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Category", "Amount", "Available_Balance"])

def read_expenses():
    expenses = []
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 4:
                    date, name, category, amount = row[:4]
                    expenses.append((date, Expense(name, category, amount)))
    except FileNotFoundError:
        pass
    return expenses

def add_expense(name, category, amount):
    expenses = read_expenses()
    total_spent = sum(exp.amount for _, exp in expenses)
    new_total_spent = total_spent + amount
    balance = st.session_state["budget"] - new_total_spent
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            name,
            category,
            "{:.2f}".format(amount),
            "{:.2f}".format(balance)
        ])

# Add Expense Form
with st.form("Add Expense"):
    st.subheader("Add a New Expense")
    name = st.text_input("Expense Name")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Expense")
    if submitted and name and category and amount > 0:
        add_expense(name, category, amount)
        st.success("Expense added!")

# Show Expenses
expenses = read_expenses()
if expenses:
    st.subheader("All Expenses")
    df_expenses = pd.DataFrame(
        [
            [date, exp.name, exp.category, "{:.2f}".format(exp.amount)]
            for date, exp in expenses
        ],
        columns=["Date", "Name", "Category", "Amount"]
    )
    st.table(df_expenses)

    total_spent = sum(exp.amount for _, exp in expenses)
    st.info(f"**Total spent:** ${total_spent:.2f}")
    st.info(f"**Budget left:** ${st.session_state['budget'] - total_spent:.2f}")

    # Category Summary
    category_totals = {}
    for _, exp in expenses:
        category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
    st.subheader("Summary by Category")
    df = pd.DataFrame(
        [(cat, "{:.2f}".format(amt)) for cat, amt in category_totals.items()],
        columns=["Category", "Total"]
    )
    st.table(df)

    # Daily Budget Estimate
    today = datetime.now().day
    next_month = datetime.now().replace(day=28) + timedelta(days=4)
    days_in_month = (next_month - timedelta(days=next_month.day)).day
    days_left = days_in_month - today
    budget_left = st.session_state["budget"] - total_spent
    if days_left > 0:
        st.info(f"**Estimated daily budget left:** ${budget_left/days_left:.2f} per day")
    else:
        st.warning("Month has ended.")
else:
    st.info("No expenses yet. Add your first expense!")

st.sidebar.markdown("---")
st.sidebar.write("Expense Tracker by [NITHIN KUMAR]")