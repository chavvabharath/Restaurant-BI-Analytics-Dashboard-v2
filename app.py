import streamlit as st

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------
# Login Screen
# ----------------------------
if not st.session_state.logged_in:

    st.title("🍽 Restaurant BI Login")
    st.markdown("Please enter your credentials to access the Restaurant BI Dashboard.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ----------------------------
# Dashboard Starts Here
# ----------------------------

import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Restaurant BI Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/restaurant_sales.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset.\n\n{e}")
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🍽️ Restaurant BI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "💰 Sales",
        "📦 Inventory",
        "📈 Customer Insights",
        "📊 Reports"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("Restaurant BI Dashboard")
st.sidebar.write("Version 1.0")

# ======================================================
# DASHBOARD
# ======================================================

if page == "🏠 Dashboard":

    st.title("🍽️ Restaurant Business Intelligence Dashboard")
    st.success("Welcome Bharath!")

    total_sales = df["Sales"].sum()
    total_bill = df["Total_Bill"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_customers = df["Customer_ID"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("💰 Sales", f"£{total_sales:,.2f}")
    col2.metric("🧾 Revenue", f"£{total_bill:,.2f}")
    col3.metric("📦 Orders", total_orders)
    col4.metric("👥 Customers", total_customers)
    col5.metric("📈 Profit", f"£{total_profit:,.2f}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly Sales")

        monthly = (
            df.groupby("Month")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(monthly)

    with right:
        st.subheader("Payment Methods")

        payment = df["Payment_Method"].value_counts()

        st.bar_chart(payment)

    left, right = st.columns(2)

    with left:
        st.subheader("Category Sales")

        category = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(category)

    with right:
        st.subheader("Top Selling Items")

        items = (
            df.groupby("Item")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(items)

    st.markdown("---")

    st.subheader("Average Customer Rating")

    st.metric("⭐ Rating", round(df["Rating"].mean(), 2))

    st.markdown("---")

    st.subheader("Restaurant Dataset")

    st.dataframe(df, use_container_width=True)

# ======================================================
# SALES
# ======================================================

elif page == "💰 Sales":

    st.title("Sales Analytics")

    st.metric("Total Sales", f"£{df['Sales'].sum():,.2f}")

    st.metric("Total Revenue", f"£{df['Total_Bill'].sum():,.2f}")

    st.subheader("Sales by Order Type")

    order = (
        df.groupby("Order_Type")["Sales"]
        .sum()
    )

    st.bar_chart(order)

    st.subheader("Sales by Waiter")

    waiter = (
        df.groupby("Waiter")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(waiter)

# ======================================================
# INVENTORY
# ======================================================

elif page == "📦 Inventory":

    st.title("Inventory")

    inventory = (
        df.groupby("Item")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    st.dataframe(inventory)

# ======================================================
# CUSTOMER
# ======================================================

elif page == "📈 Customer Insights":

    st.title("Customer Insights")

    gender = df["Gender"].value_counts()

    st.subheader("Gender Distribution")

    st.bar_chart(gender)

    customer = df["Customer_Type"].value_counts()

    st.subheader("Customer Type")

    st.bar_chart(customer)

# ======================================================
# REPORTS
# ======================================================

elif page == "📊 Reports":

    st.title("Reports")

    st.write("Dataset Summary")

    st.write(df.describe())

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="restaurant_sales.csv",
        mime="text/csv"
    )