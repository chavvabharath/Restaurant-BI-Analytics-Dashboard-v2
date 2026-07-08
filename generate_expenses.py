import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

expense_categories = [
    "Food Supplies",
    "Staff Salary",
    "Rent",
    "Electricity",
    "Gas",
    "Water",
    "Internet",
    "Marketing",
    "Kitchen Equipment",
    "Cleaning",
    "Maintenance",
    "Packaging"
]

payment_methods = [
    "Bank Transfer",
    "Cash",
    "Credit Card"
]

suppliers = [
    "Fresh Foods Ltd",
    "Metro Wholesale",
    "ABC Suppliers",
    "Kitchen World",
    "Utility Services",
    "City Market"
]

start_date = datetime(2025, 1, 1)

rows = []

for i in range(1, 1001):

    date = start_date + timedelta(days=random.randint(0, 364))

    category = random.choice(expense_categories)

    amount = round(random.uniform(20, 5000), 2)

    supplier = random.choice(suppliers)

    payment = random.choice(payment_methods)

    rows.append([
        i,
        date.strftime("%d-%m-%Y"),
        date.strftime("%B"),
        date.strftime("%A"),
        category,
        supplier,
        payment,
        amount
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "Expense_ID",
        "Date",
        "Month",
        "Day",
        "Expense_Category",
        "Supplier",
        "Payment_Method",
        "Amount"
    ]
)

df.to_csv("data/expenses.csv", index=False)

print("✅ expenses.csv created successfully!")
print(df.head())