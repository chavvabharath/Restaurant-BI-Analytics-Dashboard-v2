import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Smart Business Alerts",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Smart Business Alerts")
st.markdown("### AI Powered Restaurant Monitoring System")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/restaurant.db")

sales = pd.read_csv("data/restaurant_sales.csv")
expenses = pd.read_csv("data/expenses.csv")
inventory = pd.read_csv("data/inventory.csv")

sales.to_sql("sales", conn, if_exists="replace", index=False)
expenses.to_sql("expenses", conn, if_exists="replace", index=False)
inventory.to_sql("inventory", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database Created Successfully")

# -----------------------------------------------------
# Calculate KPIs
# -----------------------------------------------------

total_sales = sales["Total_Bill"].sum()

total_expenses = expenses["Amount"].sum()

profit = total_sales - total_expenses

profit_margin = (profit / total_sales) * 100

total_orders = len(sales)

total_customers = sales["Customer_ID"].nunique()

# -----------------------------------------------------
# KPI Cards
# -----------------------------------------------------

st.subheader("📊 Business Overview")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"£{total_sales:,.2f}"
)

col2.metric(
    "💸 Expenses",
    f"£{total_expenses:,.2f}"
)

col3.metric(
    "📈 Profit",
    f"£{profit:,.2f}"
)

col4.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# -----------------------------------------------------
# Low Stock Alerts
# -----------------------------------------------------

st.subheader("📦 Low Stock Alerts")

low_stock = inventory[
    inventory["Stock"] <= inventory["Reorder_Level"]
]

if len(low_stock) == 0:

    st.success("✅ No Low Stock Alerts")

else:

    st.error(f"⚠ {len(low_stock)} Items Need Restocking")

    st.dataframe(
        low_stock,
        use_container_width=True
    )

# -----------------------------------------------------
# High Expense Alerts
# -----------------------------------------------------

st.subheader("💸 High Expense Alerts")

expense_summary = (
    expenses.groupby("Expense_Category")["Amount"]
    .sum()
    .reset_index()
)

average_expense = expense_summary["Amount"].mean()

high_expense = expense_summary[
    expense_summary["Amount"] > average_expense
]

if len(high_expense) == 0:

    st.success("✅ Expenses are under control.")

else:

    for i,row in high_expense.iterrows():

        st.warning(
            f"⚠ {row['Expense_Category']} expenses are high (£{row['Amount']:,.2f})"
        )

st.divider()

# -----------------------------------------------------
# Best Selling Item Alert
# -----------------------------------------------------

st.subheader("🏆 Best Selling Menu Item")

top_item = (
    sales.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

best_item = top_item.iloc[0]

st.success(
    f"🏆 {best_item['Item']} sold {int(best_item['Quantity'])} units."
)

# -----------------------------------------------------
# Highest Revenue Category
# -----------------------------------------------------

st.subheader("💰 Highest Revenue Category")

category_sales = (
    sales.groupby("Category")["Total_Bill"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

highest_category = category_sales.iloc[0]

st.info(
    f"🍽 {highest_category['Category']} generated £{highest_category['Total_Bill']:,.2f}"
)

st.divider()

# -----------------------------------------------------
# Customer Alerts
# -----------------------------------------------------

st.subheader("👥 Customer Insights")

customer_type = (
    sales["Customer_Type"]
    .value_counts()
)

returning = customer_type.get("Returning",0)

new = customer_type.get("New",0)

if returning > new:

    st.success(
        f"😊 Returning Customers ({returning}) are higher than New Customers ({new})."
    )

else:

    st.warning(
        f"⚠ New Customers ({new}) exceed Returning Customers ({returning}). Consider loyalty programs."
    )

# -----------------------------------------------------
# Payment Method Alert
# -----------------------------------------------------

st.subheader("💳 Payment Method Usage")

payment = (
    sales["Payment_Method"]
    .value_counts()
    .reset_index()
)

payment.columns = [
    "Payment Method",
    "Transactions"
]

fig = px.pie(
    payment,
    names="Payment Method",
    values="Transactions",
    title="Payment Method Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------------------------
# Inventory Status Chart
# -----------------------------------------------------

st.subheader("📦 Inventory Status")

inventory_status = (
    inventory["Stock_Status"]
    .value_counts()
    .reset_index()
)

inventory_status.columns = [
    "Status",
    "Items"
]

fig2 = px.bar(
    inventory_status,
    x="Status",
    y="Items",
    color="Status",
    title="Inventory Status"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# -----------------------------------------------------
# Monthly Sales Trend
# -----------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = (
    sales.groupby("Month")["Total_Bill"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig3 = px.line(
    monthly_sales,
    x="Month",
    y="Total_Bill",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Monthly Expense Trend
# -----------------------------------------------------

st.subheader("💸 Monthly Expense Trend")

monthly_expense = (
    expenses.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

monthly_expense["Month"] = pd.Categorical(
    monthly_expense["Month"],
    categories=month_order,
    ordered=True
)

monthly_expense = monthly_expense.sort_values("Month")

fig4 = px.line(
    monthly_expense,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Expenses"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Supplier Alerts
# -----------------------------------------------------

st.subheader("🏭 Supplier Analysis")

supplier_expense = (
    expenses.groupby("Supplier")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

highest_supplier = supplier_expense.iloc[0]

st.warning(
    f"💰 Highest spending supplier: {highest_supplier['Supplier']} "
    f"(£{highest_supplier['Amount']:,.2f})"
)

fig5 = px.bar(
    supplier_expense,
    x="Supplier",
    y="Amount",
    color="Amount",
    title="Supplier Expenses"
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Business Risk Score
# -----------------------------------------------------

st.subheader("🚨 Business Risk Score")

risk_score = 100

if len(low_stock) > 5:
    risk_score -= 20

if total_expenses > total_sales * 0.70:
    risk_score -= 20

if profit_margin < 20:
    risk_score -= 20

if new > returning:
    risk_score -= 10

risk_score = max(risk_score, 0)

st.metric("Business Risk Score", f"{risk_score}/100")
st.progress(risk_score / 100)

if risk_score >= 85:
    st.success("🟢 Low Risk - Business is performing very well.")
elif risk_score >= 60:
    st.warning("🟡 Medium Risk - Monitor business performance.")
else:
    st.error("🔴 High Risk - Immediate action recommended.")

st.divider()

# -----------------------------------------------------
# AI Recommendation Engine
# -----------------------------------------------------

st.subheader("🤖 AI Business Recommendations")

recommendations = []

if len(low_stock) > 0:
    recommendations.append(
        f"📦 Restock {len(low_stock)} inventory item(s) immediately."
    )

if total_expenses > total_sales * 0.60:
    recommendations.append(
        "💸 Expenses are relatively high. Review supplier contracts and operating costs."
    )

if profit_margin < 25:
    recommendations.append(
        "📉 Profit margin is low. Consider increasing prices or reducing costs."
    )

top_item_name = best_item["Item"]

recommendations.append(
    f"🏆 Promote '{top_item_name}' because it is your best-selling menu item."
)

if returning > new:
    recommendations.append(
        "😊 Continue loyalty programmes to retain returning customers."
    )
else:
    recommendations.append(
        "🎁 Launch promotions to encourage repeat visits."
    )

highest_supplier_name = highest_supplier["Supplier"]

recommendations.append(
    f"🤝 Review spending with supplier '{highest_supplier_name}' for possible savings."
)

for rec in recommendations:
    st.success(rec)

st.divider()

# -----------------------------------------------------
# Executive Alert Summary
# -----------------------------------------------------

st.subheader("📋 Executive Alert Summary")

summary = pd.DataFrame({
    "Metric": [
        "Revenue",
        "Expenses",
        "Profit",
        "Profit Margin",
        "Orders",
        "Customers",
        "Low Stock Items",
        "Business Risk Score"
    ],
    "Value": [
        f"£{total_sales:,.2f}",
        f"£{total_expenses:,.2f}",
        f"£{profit:,.2f}",
        f"{profit_margin:.2f}%",
        total_orders,
        total_customers,
        len(low_stock),
        f"{risk_score}/100"
    ]
})

st.dataframe(summary, use_container_width=True)

st.divider()

# -----------------------------------------------------
# Alert Priority
# -----------------------------------------------------

st.subheader("🚦Alert Priority")

if risk_score >= 85:
    st.success("""
🟢 Priority Level: LOW

Business performance is healthy.
Continue monitoring operations.
""")

elif risk_score >= 60:
    st.warning("""
🟡 Priority Level: MEDIUM

Some business areas require attention.
Review expenses and inventory.
""")

else:
    st.error("""
🔴 Priority Level: HIGH

Critical business issues detected.
Immediate action is recommended.
""")

st.divider()

# -----------------------------------------------------
# Alerts Report Download (CSV)
# -----------------------------------------------------

st.subheader("📥 Download Alerts Report")

report = summary.copy()

csv = report.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Smart Alerts Report",
    data=csv,
    file_name="Smart_Business_Alerts_Report.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------------------------------
# Footer
# -----------------------------------------------------

st.caption(
    "Restaurant BI Dashboard | Smart Business Alerts | Version 1.0"
)

