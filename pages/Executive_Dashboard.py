import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("📊 Executive Dashboard")
st.markdown("### Restaurant Business Performance Overview")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
import sqlite3

conn = sqlite3.connect("database/restaurant.db")

sales = pd.read_sql("SELECT * FROM sales", conn)

expenses = pd.read_sql("SELECT * FROM expenses", conn)

inventory = pd.read_sql("SELECT * FROM inventory", conn)

employees = pd.read_sql("SELECT * FROM employees", conn)

conn.close()

# ---------------------------------------------------
# Calculate KPIs
# ---------------------------------------------------
total_revenue = sales["Total_Bill"].sum()

total_expenses = expenses["Amount"].sum()

net_profit = total_revenue - total_expenses

total_orders = len(sales)

total_customers = sales["Customer_ID"].nunique()

total_employees = len(employees)

inventory_value = (
    inventory["Stock"] *
    inventory["Unit_Price"]
).sum()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"£{total_revenue:,.2f}"
)

col2.metric(
    "💸 Expenses",
    f"£{total_expenses:,.2f}"
)

col3.metric(
    "📈 Net Profit",
    f"£{net_profit:,.2f}"
)

col4.metric(
    "👥 Employees",
    total_employees
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "🛒 Orders",
    total_orders
)

col6.metric(
    "🙋 Customers",
    total_customers
)

col7.metric(
    "📦 Inventory Value",
    f"£{inventory_value:,.2f}"
)

st.divider()

# ---------------------------------------------------
# Revenue by Month
# ---------------------------------------------------
st.subheader("📅 Monthly Revenue")

monthly_sales = sales.groupby("Month")["Total_Bill"].sum().reset_index()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig1 = px.bar(
    monthly_sales,
    x="Month",
    y="Total_Bill",
    color="Month",
    title="Monthly Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# Expense by Category
# ---------------------------------------------------
st.subheader("💸 Expense Distribution")

expense_chart = expenses.groupby("Expense_Category")["Amount"].sum().reset_index()

fig2 = px.pie(
    expense_chart,
    names="Expense_Category",
    values="Amount",
    hole=0.45,
    title="Expenses by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Customer Type
# ---------------------------------------------------
st.subheader("👥 Customer Type")

customer_chart = sales["Customer_Type"].value_counts().reset_index()

customer_chart.columns = [
    "Customer Type",
    "Count"
]

fig3 = px.bar(
    customer_chart,
    x="Customer Type",
    y="Count",
    color="Customer Type"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Gender Distribution
# ---------------------------------------------------
st.subheader("🚻 Customer Gender")

gender = sales["Gender"].value_counts().reset_index()

gender.columns = [
    "Gender",
    "Count"
]

fig4 = px.pie(
    gender,
    names="Gender",
    values="Count"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# Inventory Status
# ---------------------------------------------------
st.subheader("📦 Inventory Stock")

inventory_chart = inventory.sort_values(
    "Stock",
    ascending=False
)

fig5 = px.bar(
    inventory_chart,
    x="Item",
    y="Stock",
    color="Category",
    title="Current Inventory"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# Employee Department
# ---------------------------------------------------
st.subheader("👨‍🍳 Employees by Department")

department = employees["Role"].value_counts().reset_index()

department.columns = [
    "Role",
    "Employees"
]

fig6 = px.bar(
    department,
    x="Role",
    y="Employees",
    color="Role"
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------------------------------------------
# Top Selling Items
# ---------------------------------------------------
st.subheader("🏆 Top 10 Selling Items")

top_items = (
    sales.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig7 = px.bar(
    top_items,
    x="Item",
    y="Quantity",
    color="Quantity"
)

st.plotly_chart(fig7, use_container_width=True)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------
st.subheader("📄 Sales Data")

st.dataframe(sales)

st.subheader("📄 Expense Data")

st.dataframe(expenses)

st.subheader("📄 Employee Data")

st.dataframe(employees)

st.subheader("📄 Inventory Data")

st.dataframe(inventory)    