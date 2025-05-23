import csv
import os
from datetime import datetime, timedelta
from expense import Expense

CSV_FILE = "expenses.csv"
MONTHLY_BUDGET = 2000  # You can change this as needed

# Write header row if file does not exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Category", "Amount", "Available_Balance"])

def add_expense():
    global MONTHLY_BUDGET
    # Read previous expenses to calculate spent so far
    expenses = read_expenses()
    total_spent = sum(exp.amount for _, exp in expenses)
    name = input("Enter expense name: ")
    category = input("Enter expense category: ")
    while True:
        try:
            amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Please enter a valid number for amount.")
    expense = Expense(name, category, amount)
    new_total_spent = total_spent + amount
    balance = MONTHLY_BUDGET - new_total_spent

    # Write to CSV with balance
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), name, category, amount, balance])
    print("Expense added!")

def read_expenses():
    expenses = []
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if len(row) >= 4:
                    date, name, category, amount = row[:4]
                    expenses.append((date, Expense(name, category, amount)))
    except FileNotFoundError:
        pass
    return expenses

def summarize_expenses(expenses):
    total = sum(exp.amount for _, exp in expenses)
    print(f"\nTotal spent this month: ${total:.2f}")
    print(f"Budget left: ${MONTHLY_BUDGET - total:.2f}")
    return total

def summarize_by_category(expenses):
    category_totals = {}
    for _, exp in expenses:
        category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
    print("\nExpenses by category:")
    for cat, amt in category_totals.items():
        print(f"  {cat}: ${amt:.2f}")

def estimate_daily_budget_left(total_spent):
    today = datetime.now().day
    # Calculate days left in this month
    next_month = datetime.now().replace(day=28) + timedelta(days=4)
    days_in_month = (next_month - timedelta(days=next_month.day)).day
    days_left = days_in_month - today
    budget_left = MONTHLY_BUDGET - total_spent
    if days_left > 0:
        print(f"\nEstimated daily budget left: ${budget_left/days_left:.2f} per day")
    else:
        print("\nMonth has ended.")

def change_budget():
    global MONTHLY_BUDGET
    try:
        new_budget = float(input("Enter new monthly budget: "))
        MONTHLY_BUDGET = new_budget
        print(f"Monthly budget successfully changed to ${MONTHLY_BUDGET:.2f}")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    print("Welcome to Expense Tracker!")
    while True:
        print("\nChoose an option:")
        print("1. Add expense")
        print("2. Show summary")
        print("3. Show summary by category")
        print("4. Estimate daily budget left")
        print("5. Change monthly budget")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            expenses = read_expenses()
            summarize_expenses(expenses)
        elif choice == "3":
            expenses = read_expenses()
            summarize_by_category(expenses)
        elif choice == "4":
            expenses = read_expenses()
            total = summarize_expenses(expenses)
            estimate_daily_budget_left(total)
        elif choice == "5":
            change_budget()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()