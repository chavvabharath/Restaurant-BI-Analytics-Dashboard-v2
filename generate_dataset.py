import pandas as pd
import random
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

random.seed(42)

menu = {
    "Starters": [
        ("Spring Rolls", 6.99),
        ("Garlic Bread", 4.99),
        ("Chicken Wings", 8.99),
        ("Soup", 5.99)
    ],
    "Main Course": [
        ("Chicken Biryani", 14.99),
        ("Veg Biryani", 12.99),
        ("Butter Chicken", 15.99),
        ("Paneer Butter Masala", 13.99),
        ("Pizza", 16.99),
        ("Burger", 11.99),
        ("Pasta", 13.49),
        ("Fish & Chips", 17.99)
    ],
    "Desserts": [
        ("Ice Cream", 4.99),
        ("Brownie", 5.99),
        ("Cheesecake", 6.99)
    ],
    "Drinks": [
        ("Coke", 2.99),
        ("Coffee", 3.99),
        ("Tea", 2.49),
        ("Fresh Juice", 4.49)
    ]
}

payment_methods = [
    "Cash",
    "Card",
    "Apple Pay",
    "Google Pay",
    "Online"
]

order_types = [
    "Dine-in",
    "Takeaway",
    "Delivery"
]

customer_types = [
    "New",
    "Returning"
]

waiters = [
    "James",
    "Sophia",
    "Daniel",
    "Emma",
    "Michael",
    "Olivia",
    "David",
    "Emily"
]

rows = []

start_date = datetime(2025, 1, 1)

for i in range(1, 1001):

    date = start_date + timedelta(days=random.randint(0, 364))

    category = random.choice(list(menu.keys()))

    item, price = random.choice(menu[category])

    quantity = random.randint(1, 5)

    sales = round(price * quantity, 2)

    discount = round(random.uniform(0, sales * 0.15), 2)

    tax = round((sales - discount) * 0.20, 2)

    total = round(sales - discount + tax, 2)

    profit = round((sales - discount) * random.uniform(0.25, 0.40), 2)

    rows.append({
        "Order_ID": f"ORD{i:05}",
        "Date": date.strftime("%Y-%m-%d"),
        "Time": fake.time(),
        "Month": date.strftime("%B"),
        "Day": date.strftime("%A"),
        "Customer_ID": f"CUST{random.randint(1000,9999)}",
        "Customer_Type": random.choice(customer_types),
        "Gender": random.choice(["Male","Female"]),
        "Age": random.randint(18,65),
        "Table_No": random.randint(1,20),
        "Waiter": random.choice(waiters),
        "Category": category,
        "Item": item,
        "Quantity": quantity,
        "Unit_Price": price,
        "Sales": sales,
        "Discount": discount,
        "Tax": tax,
        "Total_Bill": total,
        "Payment_Method": random.choice(payment_methods),
        "Order_Type": random.choice(order_types),
        "Rating": random.randint(3,5),
        "Profit": profit
    })

df = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)

df.to_csv("data/restaurant_sales.csv", index=False)

print("Dataset generated successfully!")
print(df.head())
print(f"\nTotal Records: {len(df)}")