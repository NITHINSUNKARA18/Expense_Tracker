# Expense Tracker Web App

A simple, interactive expense tracker built with Python and Streamlit. Track your purchases, monitor your spending by category, and manage your monthly budget—all in a user-friendly web interface.

## Features

- **Add Expenses:** Log purchases with name, category, and amount.
- **Dynamic Budget:** Set a custom monthly budget or use the default.
- **Expense Overview:** View all expenses in a sortable table.
- **Budget Summary:** Instantly see total spent and amount left.
- **Category Breakdown:** Visualize spending by category with charts.
- **Data Persistence:** Expenses are saved in a CSV file for each session.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NITHINSUNKARA18/Expense_Tracker.git
cd expense-tracker
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.  
Install required libraries with pip:

```bash
pip install streamlit
```

If you use category charts, you may also want:

```bash
pip install pandas matplotlib
```

### 3. Project Structure

```
expense-tracker/
├── expense.py
├── streamlit_app.py
├── expenses.csv            # Created automatically after first run
└── README.md
```

- `expense.py`: Defines the Expense class.
- `streamlit_app.py`: Main Streamlit web app.
- `expenses.csv`: Your logged expenses (auto-generated).

### 4. Run the Web App

```bash
streamlit run streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. **Set Your Budget:** Use the sidebar to enter your monthly budget, or keep the default.
2. **Add Expenses:** Fill in the expense name, category, and amount, then click "Add Expense".
3. **View Summary:** See all your expenses, total spent, and remaining budget on the main page.
4. **Analyze Spending:** Visual summaries by category help you understand your spending habits.

## Customization

- To persist the budget across sessions, consider saving it to a file or database.
- You can expand the app with features like editing/deleting expenses, filtering by date, or exporting data.


## License

This project is open source. Feel free to use, modify, or distribute as needed.

---

**Happy tracking!**