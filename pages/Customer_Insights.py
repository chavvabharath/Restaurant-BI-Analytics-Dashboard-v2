import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

conn = sqlite3.connect("database/restaurant.db")

df = pd.read_sql("SELECT * FROM sales", conn)

conn.close()

st.set_page_config(page_title="Customer Insights", layout="wide")

st.title("👥 Customer Insights Dashboard")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# ---------------- KPIs ----------------

total_customers = df["Customer_ID"].nunique()
new_customers = (df["Customer_Type"] == "New").sum()
returning_customers = (df["Customer_Type"] == "Returning").sum()
avg_bill = df["Total_Bill"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", total_customers)
col2.metric("New Customers", new_customers)
col3.metric("Returning", returning_customers)
col4.metric("Average Bill (£)", f"{avg_bill:.2f}")

st.markdown("---")

# ---------------- Gender ----------------

st.subheader("👨 Gender Distribution")

gender = df.groupby("Gender").size().reset_index(name="Count")

fig = px.pie(
    gender,
    names="Gender",
    values="Count",
    hole=0.5
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Age ----------------

st.subheader("🎂 Age Distribution")

fig2 = px.histogram(
    df,
    x="Age",
    nbins=10,
    color="Gender"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- Customer Type ----------------

st.subheader("👥 Customer Type")

customer = (
    df.groupby("Customer_Type")
      .size()
      .reset_index(name="Count")
)

fig3 = px.bar(
    customer,
    x="Customer_Type",
    y="Count",
    color="Customer_Type",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- Spending ----------------

st.subheader("💷 Spending by Customer Type")

spending = (
    df.groupby("Customer_Type")["Total_Bill"]
      .mean()
      .reset_index()
)

fig4 = px.bar(
    spending,
    x="Customer_Type",
    y="Total_Bill",
    color="Customer_Type",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- Peak Hours ----------------

st.subheader("⏰ Peak Hours")

hours = (
    df.groupby("Time")
      .size()
      .reset_index(name="Orders")
)

fig5 = px.line(
    hours,
    x="Time",
    y="Orders",
    markers=True
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- Ratings ----------------

st.subheader("⭐ Customer Ratings")

fig6 = px.histogram(
    df,
    x="Rating",
    nbins=5
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------- Data ----------------

st.subheader("📋 Customer Records")

st.dataframe(df, use_container_width=True)