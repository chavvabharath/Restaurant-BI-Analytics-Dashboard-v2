import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Business Comparison",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Comparison Dashboard")
st.markdown("### Compare Restaurant Performance Between Two Months")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect Database
conn = sqlite3.connect("database/restaurant.db")

# Read Tables
sales = pd.read_sql("SELECT * FROM sales", conn)

expenses = pd.read_sql("SELECT * FROM expenses", conn)


# Your existing dashboard code goes here...

conn.close()

# -----------------------------------------------------
# Month Order
# -----------------------------------------------------

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

st.sidebar.header("📅 Select Months")

month1 = st.sidebar.selectbox(
    "Month 1",
    month_order,
    index=0
)

month2 = st.sidebar.selectbox(
    "Month 2",
    month_order,
    index=1
)

# -----------------------------------------------------
# Filter Data
# -----------------------------------------------------

sales1 = sales[sales["Month"] == month1]
sales2 = sales[sales["Month"] == month2]

expense1 = expenses[expenses["Month"] == month1]
expense2 = expenses[expenses["Month"] == month2]

# -----------------------------------------------------
# Revenue
# -----------------------------------------------------

revenue1 = sales1["Total_Bill"].sum()
revenue2 = sales2["Total_Bill"].sum()

# -----------------------------------------------------
# Expenses
# -----------------------------------------------------

expense_total1 = expense1["Amount"].sum()
expense_total2 = expense2["Amount"].sum()

# -----------------------------------------------------
# Profit
# -----------------------------------------------------

profit1 = revenue1 - expense_total1
profit2 = revenue2 - expense_total2

# -----------------------------------------------------
# Orders
# -----------------------------------------------------

orders1 = len(sales1)
orders2 = len(sales2)

# -----------------------------------------------------
# Customers
# -----------------------------------------------------

customers1 = sales1["Customer_ID"].nunique()
customers2 = sales2["Customer_ID"].nunique()

# -----------------------------------------------------
# Average Order Value
# -----------------------------------------------------

aov1 = revenue1 / orders1 if orders1 > 0 else 0
aov2 = revenue2 / orders2 if orders2 > 0 else 0

# -----------------------------------------------------
# Percentage Change Function
# -----------------------------------------------------

def percentage_change(old, new):

    if old == 0:
        return 0

    return ((new - old) / old) * 100

# -----------------------------------------------------
# KPI Cards
# -----------------------------------------------------

st.subheader("📌 Key Performance Comparison")

col1, col2 = st.columns(2)

with col1:

    st.info(f"### {month1}")

    st.metric(
        "Revenue",
        f"£{revenue1:,.2f}"
    )

    st.metric(
        "Expenses",
        f"£{expense_total1:,.2f}"
    )

    st.metric(
        "Profit",
        f"£{profit1:,.2f}"
    )

    st.metric(
        "Orders",
        orders1
    )

    st.metric(
        "Customers",
        customers1
    )

    st.metric(
        "Average Order",
        f"£{aov1:,.2f}"
    )

with col2:

    st.success(f"### {month2}")

    st.metric(
        "Revenue",
        f"£{revenue2:,.2f}",
        f"{percentage_change(revenue1,revenue2):.2f}%"
    )

    st.metric(
        "Expenses",
        f"£{expense_total2:,.2f}",
        f"{percentage_change(expense_total1,expense_total2):.2f}%"
    )

    st.metric(
        "Profit",
        f"£{profit2:,.2f}",
        f"{percentage_change(profit1,profit2):.2f}%"
    )

    st.metric(
        "Orders",
        orders2,
        f"{percentage_change(orders1,orders2):.2f}%"
    )

    st.metric(
        "Customers",
        customers2,
        f"{percentage_change(customers1,customers2):.2f}%"
    )

    st.metric(
        "Average Order",
        f"£{aov2:,.2f}",
        f"{percentage_change(aov1,aov2):.2f}%"
    )

st.divider()

# -----------------------------------------------------
# Revenue Comparison Chart
# -----------------------------------------------------

st.subheader("💰 Revenue Comparison")

revenue_chart = pd.DataFrame({

    "Month":[month1,month2],

    "Revenue":[revenue1,revenue2]

})

fig1 = px.bar(

    revenue_chart,

    x="Month",

    y="Revenue",

    color="Month",

    text_auto=True,

    title="Revenue Comparison"

)

st.plotly_chart(fig1,use_container_width=True)

# -----------------------------------------------------
# Expense Comparison
# -----------------------------------------------------

st.subheader("💸 Expense Comparison")

expense_chart = pd.DataFrame({

    "Month":[month1,month2],

    "Expenses":[expense_total1,expense_total2]

})

fig2 = px.bar(

    expense_chart,

    x="Month",

    y="Expenses",

    color="Month",

    text_auto=True,

    title="Expense Comparison"

)

st.plotly_chart(fig2,use_container_width=True)

# -----------------------------------------------------
# Profit Comparison
# -----------------------------------------------------

st.subheader("📈 Profit Comparison")

profit_chart = pd.DataFrame({

    "Month":[month1,month2],

    "Profit":[profit1,profit2]

})

fig3 = px.bar(

    profit_chart,

    x="Month",

    y="Profit",

    color="Month",

    text_auto=True,

    title="Profit Comparison"

)

st.plotly_chart(fig3,use_container_width=True)

st.divider()

# -----------------------------------------------------
# Top Selling Items Comparison
# -----------------------------------------------------

st.subheader("🏆 Top Selling Items Comparison")

top1 = (
    sales1.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top2 = (
    sales2.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"### {month1}")

    fig4 = px.bar(
        top1,
        x="Item",
        y="Quantity",
        color="Quantity",
        title=f"Top Selling Items - {month1}"
    )

    st.plotly_chart(fig4, use_container_width=True)

with col2:

    st.markdown(f"### {month2}")

    fig5 = px.bar(
        top2,
        x="Item",
        y="Quantity",
        color="Quantity",
        title=f"Top Selling Items - {month2}"
    )

    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Category Sales Comparison
# -----------------------------------------------------

st.subheader("🍽 Category Revenue Comparison")

category1 = (
    sales1.groupby("Category")["Total_Bill"]
    .sum()
    .reset_index()
)

category2 = (
    sales2.groupby("Category")["Total_Bill"]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig6 = px.pie(
        category1,
        names="Category",
        values="Total_Bill",
        hole=0.4,
        title=f"{month1}"
    )

    st.plotly_chart(fig6, use_container_width=True)

with col2:

    fig7 = px.pie(
        category2,
        names="Category",
        values="Total_Bill",
        hole=0.4,
        title=f"{month2}"
    )

    st.plotly_chart(fig7, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Payment Method Comparison
# -----------------------------------------------------

st.subheader("💳 Payment Method Comparison")

payment1 = (
    sales1["Payment_Method"]
    .value_counts()
    .reset_index()
)

payment1.columns = ["Payment Method", "Transactions"]

payment2 = (
    sales2["Payment_Method"]
    .value_counts()
    .reset_index()
)

payment2.columns = ["Payment Method", "Transactions"]

col1, col2 = st.columns(2)

with col1:

    fig8 = px.bar(
        payment1,
        x="Payment Method",
        y="Transactions",
        color="Payment Method",
        title=f"{month1}"
    )

    st.plotly_chart(fig8, use_container_width=True)

with col2:

    fig9 = px.bar(
        payment2,
        x="Payment Method",
        y="Transactions",
        color="Payment Method",
        title=f"{month2}"
    )

    st.plotly_chart(fig9, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Waiter Performance
# -----------------------------------------------------

st.subheader("👨‍🍳 Waiter Performance Comparison")

waiter1 = (
    sales1.groupby("Waiter")["Total_Bill"]
    .sum()
    .reset_index()
)

waiter2 = (
    sales2.groupby("Waiter")["Total_Bill"]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig10 = px.bar(
        waiter1,
        x="Waiter",
        y="Total_Bill",
        color="Total_Bill",
        title=f"{month1}"
    )

    st.plotly_chart(fig10, use_container_width=True)

with col2:

    fig11 = px.bar(
        waiter2,
        x="Waiter",
        y="Total_Bill",
        color="Total_Bill",
        title=f"{month2}"
    )

    st.plotly_chart(fig11, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Customer Rating Comparison
# -----------------------------------------------------

st.subheader("⭐ Customer Rating Comparison")

rating1 = round(sales1["Rating"].mean(), 2)
rating2 = round(sales2["Rating"].mean(), 2)

col1, col2 = st.columns(2)

col1.metric(
    f"{month1} Rating",
    rating1
)

col2.metric(
    f"{month2} Rating",
    rating2,
    round(rating2 - rating1, 2)
)

st.divider()

# -----------------------------------------------------
# AI Business Insights
# -----------------------------------------------------

st.subheader("🤖 AI Business Insights")

insights = []

if revenue2 > revenue1:
    insights.append("📈 Revenue increased compared to the previous month.")
else:
    insights.append("📉 Revenue decreased compared to the previous month.")

if expense_total2 > expense_total1:
    insights.append("💸 Expenses increased. Monitor operating costs.")
else:
    insights.append("✅ Expenses decreased.")

if profit2 > profit1:
    insights.append("💰 Profit improved.")
else:
    insights.append("⚠ Profit declined.")

if customers2 > customers1:
    insights.append("👥 Customer numbers increased.")
else:
    insights.append("👥 Customer numbers decreased.")

best_item = (
    sales2.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

insights.append(f"🏆 Best-selling item in {month2}: {best_item}")

for message in insights:
    st.success(message)

st.divider()

# -----------------------------------------------------
# Executive Summary
# -----------------------------------------------------

st.subheader("📋 Executive Summary")

summary = pd.DataFrame({

    "Metric":[
        "Revenue",
        "Expenses",
        "Profit",
        "Orders",
        "Customers",
        "Average Order Value",
        "Average Rating"
    ],

    month1:[
        revenue1,
        expense_total1,
        profit1,
        orders1,
        customers1,
        round(aov1,2),
        rating1
    ],

    month2:[
        revenue2,
        expense_total2,
        profit2,
        orders2,
        customers2,
        round(aov2,2),
        rating2
    ]

})

st.dataframe(
    summary,
    use_container_width=True
)

st.divider()

# -----------------------------------------------------
# Business Recommendation Engine
# -----------------------------------------------------

st.subheader("🚀 Business Recommendations")

recommendations = []

if revenue2 < revenue1:
    recommendations.append(
        "Increase marketing campaigns to boost revenue."
    )

if expense_total2 > expense_total1:
    recommendations.append(
        "Review supplier costs and reduce unnecessary expenses."
    )

if rating2 < 4:
    recommendations.append(
        "Improve customer service and food quality."
    )

if customers2 < customers1:
    recommendations.append(
        "Introduce loyalty offers for returning customers."
    )

recommendations.append(
    f"Promote '{best_item}' because it is the best-selling menu item."
)

for rec in recommendations:

    st.info("✅ " + rec)

st.divider()

# -----------------------------------------------------
# Export Comparison Report
# -----------------------------------------------------

st.subheader("📥 Download Comparison Report")

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Business Comparison Report",
    csv,
    "Business_Comparison_Report.csv",
    "text/csv"
)

st.divider()

# -----------------------------------------------------
# Footer
# -----------------------------------------------------

st.caption(
    "Restaurant BI Dashboard | Business Comparison Dashboard | Version 1.0"
)