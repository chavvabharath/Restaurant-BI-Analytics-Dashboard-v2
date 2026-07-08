import sqlite3
import pandas as pd

conn = sqlite3.connect("database/restaurant.db")

sales = pd.read_csv("data/restaurant_sales.csv")
expenses = pd.read_csv("data/expenses.csv")
inventory = pd.read_csv("data/inventory.csv")
employees = pd.read_csv("data/employees.csv")

sales.to_sql("sales", conn, if_exists="replace", index=False)
expenses.to_sql("expenses", conn, if_exists="replace", index=False)
inventory.to_sql("inventory", conn, if_exists="replace", index=False)
employees.to_sql("employees", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database Created Successfully")