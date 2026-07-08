import streamlit as st

def apply_filters(df):

    st.sidebar.header("🔍 Dashboard Filters")

    # -----------------------------
    # Month Filter
    # -----------------------------

    months = ["All"] + sorted(df["Month"].dropna().unique().tolist())

    selected_month = st.sidebar.selectbox(
        "📅 Month",
        months
    )

    # -----------------------------
    # Category Filter
    # -----------------------------

    categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

    selected_category = st.sidebar.selectbox(
        "🍽 Category",
        categories
    )

    # -----------------------------
    # Payment Method
    # -----------------------------

    payments = ["All"] + sorted(df["Payment_Method"].dropna().unique().tolist())

    selected_payment = st.sidebar.selectbox(
        "💳 Payment",
        payments
    )

    # -----------------------------
    # Customer Type
    # -----------------------------

    customer_types = ["All"] + sorted(df["Customer_Type"].dropna().unique().tolist())

    selected_customer = st.sidebar.selectbox(
        "👥 Customer Type",
        customer_types
    )

    # -----------------------------
    # Gender
    # -----------------------------

    genders = ["All"] + sorted(df["Gender"].dropna().unique().tolist())

    selected_gender = st.sidebar.selectbox(
        "🚻 Gender",
        genders
    )

    # -----------------------------
    # Waiter
    # -----------------------------

    waiters = ["All"] + sorted(df["Waiter"].dropna().unique().tolist())

    selected_waiter = st.sidebar.selectbox(
        "👨‍🍳 Waiter",
        waiters
    )

    # -----------------------------
    # Apply Filters
    # -----------------------------

    filtered_df = df.copy()

    if selected_month != "All":
        filtered_df = filtered_df[
            filtered_df["Month"] == selected_month
        ]

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    if selected_payment != "All":
        filtered_df = filtered_df[
            filtered_df["Payment_Method"] == selected_payment
        ]

    if selected_customer != "All":
        filtered_df = filtered_df[
            filtered_df["Customer_Type"] == selected_customer
        ]

    if selected_gender != "All":
        filtered_df = filtered_df[
            filtered_df["Gender"] == selected_gender
        ]

    if selected_waiter != "All":
        filtered_df = filtered_df[
            filtered_df["Waiter"] == selected_waiter
        ]

    return filtered_df