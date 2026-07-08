import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Manager Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Manager Assistant")
st.markdown("Ask questions about your restaurant business.")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect Database
conn = sqlite3.connect("database/restaurant.db")

# Read Tables
sales = pd.read_sql("SELECT * FROM sales", conn)

expenses = pd.read_sql("SELECT * FROM expenses", conn)

inventory = pd.read_sql("SELECT * FROM inventory", conn)

employees = pd.read_sql("SELECT * FROM employees", conn)

# Your existing dashboard code goes here...

conn.close()

# --------------------------------------------------
# Calculate Business Metrics
# --------------------------------------------------

total_sales = sales["Total_Bill"].sum()
total_expenses = expenses["Amount"].sum()
profit = total_sales - total_expenses
profit_margin = (profit / total_sales) * 100

top_item = (
    sales.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

top_category = (
    expenses.groupby("Expense_Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

top_supplier = (
    expenses.groupby("Supplier")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

customer_type = (
    sales["Customer_Type"]
    .value_counts()
    .index[0]
)

gender = (
    sales["Gender"]
    .value_counts()
    .index[0]
)

highest_role = (
    employees["Role"]
    .value_counts()
    .index[0]
)

low_stock = inventory[inventory["Stock"] < 30]

inventory_value = (
    inventory["Stock"] *
    inventory["Unit_Price"]
).sum()

# --------------------------------------------------
# Health Score
# --------------------------------------------------

score = 0

if total_sales > 250000:
    score += 30
elif total_sales > 150000:
    score += 20
else:
    score += 10

if profit_margin > 30:
    score += 25
elif profit_margin > 20:
    score += 20
else:
    score += 10

expense_ratio = total_expenses / total_sales

if expense_ratio < 0.40:
    score += 20
elif expense_ratio < 0.50:
    score += 15
else:
    score += 10

if len(low_stock) < 5:
    score += 15
else:
    score += 8

return_rate = len(
    sales[sales["Customer_Type"] == "Returning"]
) / len(sales)

if return_rate > 0.50:
    score += 10
else:
    score += 5

# --------------------------------------------------
# Question Input
# --------------------------------------------------

question = st.text_input(
    "Ask a business question"
)

if st.button("Analyze"):

    q = question.lower()

    if "sales" in q or "revenue" in q:

        st.success(f"""
### Sales Analysis

💰 Total Revenue : £{total_sales:,.2f}

📈 Net Profit : £{profit:,.2f}

📊 Profit Margin : {profit_margin:.2f}%
""")

    elif "expense" in q:

        st.success(f"""
### Expense Analysis

💸 Total Expenses : £{total_expenses:,.2f}

Highest Expense Category :

✅ {top_category}

Highest Supplier :

🏢 {top_supplier}
""")

    elif "supplier" in q:

        st.success(f"""
🏢 Highest Spending Supplier

{top_supplier}

Consider negotiating better prices with this supplier.
""")

    elif "inventory" in q or "stock" in q:

        st.success(f"""
Inventory Value

£{inventory_value:,.2f}

Items with Low Stock

{len(low_stock)}
""")

        st.dataframe(low_stock)

    elif "employee" in q or "staff" in q:

        st.success(f"""
Employees

👨‍🍳 Total Employees : {len(employees)}

Most Common Role

{highest_role}
""")

    elif "customer" in q:

        st.success(f"""
Customer Insights

Most Common Customer Type

{customer_type}

Most Common Gender

{gender}

Total Customers

{sales["Customer_ID"].nunique()}
""")

    elif "health" in q or "score" in q:

        if score >= 85:
            status = "🟢 Excellent"

        elif score >= 70:
            status = "🟡 Good"

        elif score >= 50:
            status = "🟠 Average"

        else:
            status = "🔴 Poor"

        st.success(f"""
Business Health Score

{score}/100

Status

{status}
""")

    elif "best item" in q or "top item" in q or "selling" in q:

        st.success(f"""
🏆 Best Selling Item

{top_item}
""")

    elif "recommend" in q or "advice" in q:

        st.success(f"""
🤖 AI Recommendations

• Promote **{top_item}** because it is the best-selling menu item.

• Reduce spending on **{top_category}**.

• Negotiate with **{top_supplier}** to lower purchasing costs.

• Restock low inventory items.

• Focus on returning customers with loyalty offers.

• Continue monitoring monthly KPIs.
""")

    else:

        st.warning("""
I can answer questions like:

• What are today's sales?

• What is total revenue?

• What are total expenses?

• Which expense category is highest?

• Which supplier costs the most?

• Show inventory status.

• Show employee details.

• Show customer insights.

• What is the business health score?

• Give business recommendations.

• Which item sells the most?
""")

st.divider()

st.subheader("💡 Example Questions")

st.info("""
• What is total revenue?

• Show total expenses

• Which supplier costs the most?

• Which expense category is highest?

• Show inventory status

• Show employee details

• Show customer insights

• What is the business health score?

• Which item sells the most?

• Give business recommendations
""")