import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.title("📦 Inventory Dashboard")

# Load Inventory Data
import sqlite3
conn = sqlite3.connect("database/restaurant.db")
df = pd.read_sql("SELECT * FROM inventory", conn)
conn.close()

# ---------------- KPI SECTION ----------------

total_items = len(df)
total_stock = df["Stock"].sum()
low_stock = (df["Stock_Status"] == "Low Stock").sum()
avg_price = df["Unit_Price"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Inventory Items", total_items)
col2.metric("Total Stock", total_stock)
col3.metric("Low Stock Items", low_stock)
col4.metric("Average Unit Price (£)", f"{avg_price:.2f}")

st.markdown("---")

# ---------------- STOCK BY CATEGORY ----------------

st.subheader("📊 Stock by Category")

category = df.groupby("Category")["Stock"].sum().reset_index()

fig = px.bar(
    category,
    x="Category",
    y="Stock",
    color="Category",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- STOCK STATUS ----------------

st.subheader("📈 Stock Status")

status = df.groupby("Stock_Status").size().reset_index(name="Count")

fig2 = px.pie(
    status,
    names="Stock_Status",
    values="Count",
    hole=0.5
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- SUPPLIER ANALYSIS ----------------

st.subheader("🚚 Supplier Inventory")

supplier = df.groupby("Supplier")["Stock"].sum().reset_index()

fig3 = px.bar(
    supplier,
    x="Supplier",
    y="Stock",
    color="Supplier",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- SEARCH ----------------

st.subheader("🔍 Search Inventory")

search = st.text_input("Enter Item Name")

if search:
    result = df[df["Item"].str.contains(search, case=False)]
    st.dataframe(result, use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

# ---------------- LOW STOCK ALERT ----------------

st.subheader("⚠️ Low Stock Items")

low = df[df["Stock_Status"] == "Low Stock"]

if len(low) > 0:
    st.error(f"{len(low)} items need restocking!")
    st.dataframe(low, use_container_width=True)
else:
    st.success("All inventory items are sufficiently stocked.")