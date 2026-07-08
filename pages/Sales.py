import streamlit as st
import pandas as pd
import plotly.express as px

from utils.filter import apply_filters
sales = pd.read_csv("data/restaurant_sales.csv")
sales = apply_filters(sales)
total_sales = sales["Total_Bill"].sum()
st.metric("Total Sales", f"£{total_sales:,.2f}")


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Sales Analytics", layout="wide")

st.title("📈 Sales Analytics")
st.subheader("Restaurant Sales Dataset")

# -----------------------------
# LOAD DATA
# -----------------------------
import sqlite3
conn = sqlite3.connect("database/restaurant.db")
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# -----------------------------
# SHOW DATASET
# -----------------------------
st.dataframe(df, use_container_width=True)

# -----------------------------
# KPI SECTION
# -----------------------------
st.markdown("---")
st.header("📊 Sales Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        df["Order_ID"].nunique()
    )

with col2:
    st.metric(
        "Total Revenue (£)",
        f"{df['Total_Bill'].sum():,.2f}"
    )

with col3:
    st.metric(
        "Average Bill (£)",
        f"{df['Total_Bill'].mean():,.2f}"
    )

with col4:
    st.metric(
        "Customers",
        df["Customer_ID"].nunique()
    )

# -----------------------------
# DAILY SALES
# -----------------------------
st.markdown("---")
st.header("📅 Daily Sales")

daily_sales = (
    df.groupby("Date")["Total_Bill"]
      .sum()
      .reset_index()
)

fig1 = px.line(
    daily_sales,
    x="Date",
    y="Total_Bill",
    markers=True,
    title="Daily Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# MONTHLY SALES
# -----------------------------
st.markdown("---")
st.header("📆 Monthly Sales")

monthly_sales = (
    df.groupby("Month")["Total_Bill"]
      .sum()
      .reset_index()
)

fig2 = px.bar(
    monthly_sales,
    x="Month",
    y="Total_Bill",
    color="Month",
    text_auto=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# SALES BY CATEGORY
# -----------------------------
st.markdown("---")
st.header("🍽 Sales by Category")

category_sales = (
    df.groupby("Category")["Total_Bill"]
      .sum()
      .reset_index()
)

fig3 = px.bar(
    category_sales,
    x="Category",
    y="Total_Bill",
    color="Category",
    text_auto=True,
    title="Category Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# TOP SELLING ITEMS
# -----------------------------
st.markdown("---")
st.header("🏆 Top 10 Selling Items")

top_items = (
    df.groupby("Item")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig4 = px.bar(
    top_items,
    x="Quantity",
    y="Item",
    orientation="h",
    color="Quantity",
    title="Top Selling Items"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# PAYMENT METHODS
# -----------------------------
st.markdown("---")
st.header("💳 Payment Methods")

payment = (
    df.groupby("Payment_Method")
      .size()
      .reset_index(name="Count")
)

fig5 = px.pie(
    payment,
    names="Payment_Method",
    values="Count",
    hole=0.5,
    title="Payment Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# WAITER PERFORMANCE
# -----------------------------
st.markdown("---")
st.header("👨‍🍳 Waiter Performance")

waiter_sales = (
    df.groupby("Waiter")["Total_Bill"]
      .sum()
      .reset_index()
      .sort_values(by="Total_Bill", ascending=False)
)

fig6 = px.bar(
    waiter_sales,
    x="Waiter",
    y="Total_Bill",
    color="Waiter",
    text_auto=True,
    title="Revenue by Waiter"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# CUSTOMER TYPE
# -----------------------------
st.markdown("---")
st.header("👥 Customer Type")

customer_type = (
    df.groupby("Customer_Type")
      .size()
      .reset_index(name="Count")
)

fig7 = px.pie(
    customer_type,
    names="Customer_Type",
    values="Count",
    hole=0.5,
    title="New vs Returning Customers"
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# SALES BY DAY
# -----------------------------
st.markdown("---")
st.header("📅 Sales by Day")

day_sales = (
    df.groupby("Day")["Total_Bill"]
      .sum()
      .reset_index()
)

fig8 = px.bar(
    day_sales,
    x="Day",
    y="Total_Bill",
    color="Day",
    text_auto=True,
    title="Revenue by Day"
)

st.plotly_chart(fig8, use_container_width=True)

# -----------------------------
# SUMMARY TABLE
# -----------------------------
st.markdown("---")
st.header("📋 Summary Statistics")

st.dataframe(df.describe(include="all"), use_container_width=True)

st.success("✅ Sales Analytics Dashboard Loaded Successfully!")