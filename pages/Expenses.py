import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Expense Analytics",
    layout="wide"
)

st.title("💸 Expense Analytics Dashboard")

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------
import sqlite3
conn = sqlite3.connect("database/restaurant.db")
df = pd.read_sql("SELECT * FROM expenses", conn)
conn.close()

# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

total_expense = df["Amount"].sum()

average_expense = df["Amount"].mean()

transactions = len(df)

suppliers = df["Supplier"].nunique()

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "💰 Total Expenses",
    f"£{total_expense:,.2f}"
)

col2.metric(
    "📊 Average Expense",
    f"£{average_expense:,.2f}"
)

col3.metric(
    "🏢 Suppliers",
    suppliers
)

col4.metric(
    "🧾 Transactions",
    transactions
)

st.divider()

# -------------------------------------------------------
# Monthly Expenses
# -------------------------------------------------------

st.subheader("📅 Monthly Expense Trend")

months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly = (
    df.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

monthly["Month"] = pd.Categorical(
    monthly["Month"],
    categories=months,
    ordered=True
)

monthly = monthly.sort_values("Month")

fig = px.line(
    monthly,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Expenses"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# Expense Category
# -------------------------------------------------------

st.subheader("📊 Expense Categories")

category = (
    df.groupby("Expense_Category")["Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category,
    x="Expense_Category",
    y="Amount",
    color="Expense_Category",
    text_auto=".2s"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# Payment Method
# -------------------------------------------------------

st.subheader("💳 Payment Method")

payment = (
    df.groupby("Payment_Method")["Amount"]
    .sum()
    .reset_index()
)

fig = px.pie(
    payment,
    names="Payment_Method",
    values="Amount",
    hole=.45
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# Supplier Analysis
# -------------------------------------------------------

st.subheader("🏢 Supplier Analysis")

supplier = (
    df.groupby("Supplier")["Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    supplier,
    x="Supplier",
    y="Amount",
    color="Supplier",
    text_auto=".2s"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# Daily Expense
# -------------------------------------------------------

st.subheader("📈 Daily Expense Trend")

daily = (
    df.groupby("Day")["Amount"]
    .sum()
    .reset_index()
)

days = [
    "Monday","Tuesday","Wednesday","Thursday",
    "Friday","Saturday","Sunday"
]

daily["Day"] = pd.Categorical(
    daily["Day"],
    categories=days,
    ordered=True
)

daily = daily.sort_values("Day")

fig = px.line(
    daily,
    x="Day",
    y="Amount",
    markers=True
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# Top 10 Highest Expenses
# -------------------------------------------------------

st.subheader("🔥 Top 10 Highest Expenses")

top = (
    df.sort_values(
        "Amount",
        ascending=False
    )
    .head(10)
)

st.dataframe(top,use_container_width=True)

# -------------------------------------------------------
# Complete Expense Dataset
# -------------------------------------------------------

st.subheader("📄 Expense Dataset")

st.dataframe(df,use_container_width=True)

# -------------------------------------------------------
# AI Recommendation Engine
# -------------------------------------------------------

st.subheader("🤖 AI Business Recommendations")

highest = category.sort_values(
    "Amount",
    ascending=False
).iloc[0]["Expense_Category"]

highest_supplier = supplier.sort_values(
    "Amount",
    ascending=False
).iloc[0]["Supplier"]

st.success(f"""
✅ Highest expense category: **{highest}**

🏢 Highest spending supplier: **{highest_supplier}**

💡 Review supplier contracts to reduce costs.

💡 Monitor {highest} expenses monthly.

💡 Negotiate discounts with frequent suppliers.

💡 Track monthly expense growth.
""")