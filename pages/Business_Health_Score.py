import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Business Health Score",
    page_icon="💚",
    layout="wide"
)

st.title("💚 Business Health Score")
st.markdown("### Overall Performance of the Restaurant")

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
# KPI Calculations
# --------------------------------------------------

total_sales = sales["Total_Bill"].sum()

total_expenses = expenses["Amount"].sum()

profit = total_sales - total_expenses

profit_margin = (profit / total_sales) * 100

total_orders = len(sales)

total_customers = sales["Customer_ID"].nunique()

total_employees = len(employees)

inventory_value = (
    inventory["Stock"] *
    inventory["Unit_Price"]
).sum()

low_stock = len(inventory[inventory["Stock"] < 30])

# --------------------------------------------------
# Business Health Score
# --------------------------------------------------

# Sales Score (30)

if total_sales >= 250000:
    sales_score = 30
elif total_sales >= 200000:
    sales_score = 25
elif total_sales >= 150000:
    sales_score = 20
else:
    sales_score = 15

# Profit Score (25)

if profit_margin >= 35:
    profit_score = 25
elif profit_margin >= 25:
    profit_score = 20
elif profit_margin >= 15:
    profit_score = 15
else:
    profit_score = 8

# Expense Score (20)

expense_ratio = total_expenses / total_sales

if expense_ratio <= 0.40:
    expense_score = 20
elif expense_ratio <= 0.50:
    expense_score = 16
elif expense_ratio <= 0.60:
    expense_score = 12
else:
    expense_score = 8

# Inventory Score (15)

if low_stock == 0:
    inventory_score = 15
elif low_stock <= 5:
    inventory_score = 12
else:
    inventory_score = 8

# Customer Score (10)

returning = sales[sales["Customer_Type"] == "Returning"]

return_rate = len(returning) / len(sales)

if return_rate >= 0.60:
    customer_score = 10
elif return_rate >= 0.40:
    customer_score = 8
else:
    customer_score = 5

# Final Score

health_score = (
    sales_score
    + profit_score
    + expense_score
    + inventory_score
    + customer_score
)

# --------------------------------------------------
# Health Status
# --------------------------------------------------

if health_score >= 85:
    status = "🟢 Excellent"
elif health_score >= 70:
    status = "🟡 Good"
elif health_score >= 50:
    status = "🟠 Average"
else:
    status = "🔴 Poor"

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("📊 Business Overview")

col1,col2,col3,col4 = st.columns(4)

col1.metric("💰 Revenue",f"£{total_sales:,.2f}")

col2.metric("💸 Expenses",f"£{total_expenses:,.2f}")

col3.metric("📈 Profit",f"£{profit:,.2f}")

col4.metric("📊 Profit Margin",f"{profit_margin:.2f}%")

st.divider()

# --------------------------------------------------
# Business Health Score
# --------------------------------------------------

st.subheader("💚 Overall Business Health")

st.metric(
    "Business Health Score",
    f"{health_score}/100"
)

st.success(f"Current Status : {status}")

st.divider()

# --------------------------------------------------
# Score Breakdown
# --------------------------------------------------

st.subheader("📋 Score Breakdown")

score_df = pd.DataFrame({

    "Business Metric":[

        "Sales Performance",

        "Profit Margin",

        "Expense Control",

        "Inventory Health",

        "Customer Retention"

    ],

    "Score":[

        sales_score,

        profit_score,

        expense_score,

        inventory_score,

        customer_score

    ]

})

st.dataframe(score_df,use_container_width=True)

# --------------------------------------------------
# Breakdown Chart
# --------------------------------------------------

fig = px.bar(

    score_df,

    x="Business Metric",

    y="Score",

    color="Business Metric",

    text="Score",

    title="Business Health Breakdown"

)

st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------

st.subheader("📌 Executive Summary")

st.info(f"""

💰 Total Revenue : £{total_sales:,.2f}

💸 Total Expenses : £{total_expenses:,.2f}

📈 Net Profit : £{profit:,.2f}

📦 Inventory Value : £{inventory_value:,.2f}

👥 Total Employees : {total_employees}

🛒 Total Orders : {total_orders}

🙋 Total Customers : {total_customers}

""")

# --------------------------------------------------
# AI Business Recommendations
# --------------------------------------------------

st.subheader("🤖 AI Business Recommendations")

recommendations = []

if profit_margin < 20:
    recommendations.append(
        "Increase profit margin by reducing operational costs."
    )

if expense_ratio > 0.50:
    recommendations.append(
        "Expenses are high. Review supplier contracts and unnecessary spending."
    )

if low_stock > 5:
    recommendations.append(
        "Several inventory items are running low. Reorder stock soon."
    )

if return_rate < 0.50:
    recommendations.append(
        "Introduce loyalty programmes to increase repeat customers."
    )

if health_score >= 85:
    recommendations.append(
        "Overall restaurant performance is excellent. Continue monitoring KPIs."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Business performance is stable. Continue monitoring weekly."
    )

for i, rec in enumerate(recommendations, start=1):
    st.success(f"{i}. {rec}")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption("Restaurant BI Dashboard | Business Health Score")