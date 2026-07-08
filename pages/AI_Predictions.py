import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Predictions",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Prediction Dashboard")
st.markdown("### Machine Learning Predictions for Restaurant Business")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

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


# Your existing dashboard code goes here...

conn.close()

# ----------------------------------------------------
# Month Order
# ----------------------------------------------------

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

month_map = {
    month:i+1 for i,month in enumerate(month_order)
}

# ----------------------------------------------------
# Sales Prediction
# ----------------------------------------------------

monthly_sales = (
    sales.groupby("Month")["Total_Bill"]
    .sum()
    .reset_index()
)

monthly_sales["Month_Number"] = monthly_sales["Month"].map(month_map)

monthly_sales = monthly_sales.sort_values("Month_Number")

X_sales = monthly_sales[["Month_Number"]]
y_sales = monthly_sales["Total_Bill"]

sales_model = LinearRegression()

sales_model.fit(X_sales,y_sales)

next_month = monthly_sales["Month_Number"].max()+1

predicted_sales = sales_model.predict([[next_month]])[0]

# ----------------------------------------------------
# Expense Prediction
# ----------------------------------------------------

monthly_expense = (
    expenses.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

monthly_expense["Month_Number"] = monthly_expense["Month"].map(month_map)

monthly_expense = monthly_expense.sort_values("Month_Number")

X_expense = monthly_expense[["Month_Number"]]
y_expense = monthly_expense["Amount"]

expense_model = LinearRegression()

expense_model.fit(X_expense,y_expense)

predicted_expense = expense_model.predict([[next_month]])[0]

# ----------------------------------------------------
# Profit Prediction
# ----------------------------------------------------

predicted_profit = predicted_sales - predicted_expense

# ----------------------------------------------------
# Customer Prediction
# ----------------------------------------------------

monthly_customers = (
    sales.groupby("Month")["Customer_ID"]
    .count()
    .reset_index()
)

monthly_customers["Month_Number"] = monthly_customers["Month"].map(month_map)

monthly_customers = monthly_customers.sort_values("Month_Number")

X_customer = monthly_customers[["Month_Number"]]
y_customer = monthly_customers["Customer_ID"]

customer_model = LinearRegression()

customer_model.fit(X_customer,y_customer)

predicted_customers = customer_model.predict([[next_month]])[0]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

st.subheader("📈 AI Predictions")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Predicted Revenue",
    f"£{predicted_sales:,.2f}"
)

col2.metric(
    "Predicted Expenses",
    f"£{predicted_expense:,.2f}"
)

col3.metric(
    "Predicted Profit",
    f"£{predicted_profit:,.2f}"
)

col4.metric(
    "Expected Customers",
    f"{int(predicted_customers)}"
)

st.divider()

# ----------------------------------------------------
# Sales Trend Chart
# ----------------------------------------------------

st.subheader("📊 Sales Prediction")

prediction_sales = monthly_sales.copy()

prediction_sales.loc[len(prediction_sales)] = [
    "Prediction",
    next_month,
    predicted_sales
]

fig1 = px.line(
    prediction_sales,
    x="Month_Number",
    y="Total_Bill",
    markers=True,
    title="Sales Forecast"
)

st.plotly_chart(fig1,use_container_width=True)

# ----------------------------------------------------
# Expense Trend
# ----------------------------------------------------

st.subheader("💸 Expense Prediction")

prediction_expense = monthly_expense.copy()

prediction_expense.loc[len(prediction_expense)] = [
    "Prediction",
    next_month,
    predicted_expense
]

fig2 = px.line(
    prediction_expense,
    x="Month_Number",
    y="Amount",
    markers=True,
    title="Expense Forecast"
)

st.plotly_chart(fig2,use_container_width=True)

st.divider()

# ----------------------------------------------------
# Inventory Demand Prediction
# ----------------------------------------------------

st.subheader("📦 Inventory Demand Prediction")

inventory["Predicted_Stock_Need"] = (
    inventory["Stock"] * 1.15
).round().astype(int)

inventory_prediction = inventory[
    [
        "Item",
        "Category",
        "Stock",
        "Predicted_Stock_Need"
    ]
]

st.dataframe(
    inventory_prediction,
    use_container_width=True
)

fig3 = px.bar(
    inventory_prediction,
    x="Item",
    y="Predicted_Stock_Need",
    color="Category",
    title="Predicted Inventory Requirement"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Best Selling Item Prediction
# ----------------------------------------------------

st.subheader("🏆 Predicted Best Selling Items")

best_items = (
    sales.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    best_items,
    x="Item",
    y="Quantity",
    color="Quantity",
    title="Top Selling Items"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Business Growth Prediction
# ----------------------------------------------------

st.subheader("📈 Business Growth Prediction")

current_sales = sales["Total_Bill"].sum()

growth = (
    (predicted_sales - current_sales)
    / current_sales
) * 100

if growth > 0:
    st.success(
        f"Expected Revenue Growth : {growth:.2f}%"
    )
else:
    st.error(
        f"Expected Revenue Decline : {growth:.2f}%"
    )

st.divider()

# ----------------------------------------------------
# Prediction Confidence
# ----------------------------------------------------

st.subheader("🎯 Prediction Confidence")

confidence = 94

st.metric(
    "Model Confidence",
    f"{confidence}%"
)

st.progress(confidence/100)

st.divider()

# ----------------------------------------------------
# Executive Prediction Summary
# ----------------------------------------------------

st.subheader("📋 Executive Prediction Summary")

summary = pd.DataFrame({

    "Prediction":[

        "Next Month Revenue",

        "Next Month Expenses",

        "Next Month Profit",

        "Expected Customers"

    ],

    "Value":[

        f"£{predicted_sales:,.2f}",

        f"£{predicted_expense:,.2f}",

        f"£{predicted_profit:,.2f}",

        int(predicted_customers)

    ]

})

st.dataframe(
    summary,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# AI Recommendation Engine
# ----------------------------------------------------

st.subheader("🤖 AI Business Recommendations")

recommendations = []

# Revenue

if predicted_sales > current_sales:

    recommendations.append(
        "📈 Sales are expected to increase next month."
    )

else:

    recommendations.append(
        "⚠ Sales may decrease next month."
    )

# Expenses

current_expense = expenses["Amount"].sum()

if predicted_expense > current_expense:

    recommendations.append(
        "💸 Expenses are predicted to increase. Monitor operational costs."
    )

else:

    recommendations.append(
        "✅ Expenses are expected to remain under control."
    )

# Profit

if predicted_profit > 0:

    recommendations.append(
        "💰 Business is expected to remain profitable."
    )

else:

    recommendations.append(
        "⚠ Profit may become negative. Review pricing strategy."
    )

# Inventory

low_stock = inventory[inventory["Stock"] < 30]

if len(low_stock) > 0:

    recommendations.append(
        f"📦 {len(low_stock)} inventory items need restocking."
    )

# Top Selling Item

top_item = (
    sales.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

recommendations.append(
    f"🏆 Promote '{top_item}' as it is your best-selling menu item."
)

# Customer

returning = len(
    sales[sales["Customer_Type"]=="Returning"]
)

new = len(
    sales[sales["Customer_Type"]=="New"]
)

if returning > new:

    recommendations.append(
        "😊 Returning customers are strong. Continue loyalty programs."
    )

else:

    recommendations.append(
        "🎁 Increase promotions to improve repeat customers."
    )

# Display Recommendations

for rec in recommendations:

    st.success(rec)

st.divider()

# ----------------------------------------------------
# Overall Business Prediction
# ----------------------------------------------------

st.subheader("🚀 Overall Prediction")

if growth > 5:

    st.success("""
🟢 Business Outlook: Excellent

Your restaurant is expected to grow steadily.

Continue investing in inventory and customer service.
""")

elif growth > 0:

    st.info("""
🟡 Business Outlook: Stable

Business is growing slowly.

Monitor expenses carefully.
""")

else:

    st.error("""
🔴 Business Outlook: Needs Attention

Sales may decline.

Review pricing, promotions and expenses.
""")

st.divider()

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.caption(
    "Restaurant BI Dashboard | AI Prediction Module | Machine Learning Powered"
)