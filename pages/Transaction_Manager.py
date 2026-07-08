import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Transaction Manager",
    page_icon="💾",
    layout="wide"
)

st.title("💾 Sales Transaction Manager")
st.markdown("Add New Sales Transactions into SQLite Database")

# ==========================================================
# Database Connection
# ==========================================================

conn = sqlite3.connect("database/restaurant.db")
cursor = conn.cursor()

# ==========================================================
# Add Transaction
# ==========================================================

st.header("➕ Add New Sales Transaction")

with st.form("add_transaction"):

    col1, col2, col3 = st.columns(3)

    with col1:

        order_id = st.text_input(
            "Order ID",
            placeholder="ORD5001"
        )

        date = st.date_input("Date")

        time = st.text_input(
            "Time",
            value=datetime.now().strftime("%H:%M")
        )

        customer_id = st.text_input(
            "Customer ID",
            placeholder="C001"
        )

        customer_type = st.selectbox(
            "Customer Type",
            ["Member","Normal"]
        )

        gender = st.selectbox(
            "Gender",
            ["Male","Female"]
        )

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=25
        )

        table_no = st.number_input(
            "Table Number",
            min_value=1,
            value=1
        )

    with col2:

        waiter = st.text_input(
            "Waiter",
            placeholder="John"
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Beverage",
                "Dessert"
            ]
        )

        item = st.text_input(
            "Item",
            placeholder="Pizza"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        unit_price = st.number_input(
            "Unit Price (£)",
            min_value=0.0,
            value=10.0
        )

        discount = st.number_input(
            "Discount (£)",
            min_value=0.0,
            value=0.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Card",
                "UPI",
                "Online"
            ]
        )

    with col3:

        order_type = st.selectbox(
            "Order Type",
            [
                "Dine-In",
                "Takeaway",
                "Delivery"
            ]
        )

        rating = st.slider(
            "Customer Rating",
            1,
            5,
            5
        )

        tax_rate = st.number_input(
            "Tax (%)",
            value=5.0
        )

        sales = quantity * unit_price

        tax = sales * (tax_rate / 100)

        total_bill = sales - discount + tax

        profit = sales * 0.30

        st.metric(
            "Sales",
            f"£{sales:.2f}"
        )

        st.metric(
            "Tax",
            f"£{tax:.2f}"
        )

        st.metric(
            "Total Bill",
            f"£{total_bill:.2f}"
        )

        st.metric(
            "Estimated Profit",
            f"£{profit:.2f}"
        )

    submitted = st.form_submit_button("Add Transaction")

    if submitted:

        month = date.strftime("%B")
        day = date.strftime("%A")

        cursor.execute(
            "SELECT Order_ID FROM sales WHERE Order_ID=?",
            (order_id,)
        )

        existing = cursor.fetchone()

        if existing:

            st.error("❌ Order ID already exists.")

        else:

            cursor.execute("""
            INSERT INTO sales
            (
                Order_ID,
                Date,
                Time,
                Month,
                Day,
                Customer_ID,
                Customer_Type,
                Gender,
                Age,
                Table_No,
                Waiter,
                Category,
                Item,
                Quantity,
                Unit_Price,
                Sales,
                Discount,
                Tax,
                Total_Bill,
                Payment_Method,
                Order_Type,
                Rating,
                Profit
            )

            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?
            )
            """,

            (
                order_id,
                str(date),
                time,
                month,
                day,
                customer_id,
                customer_type,
                gender,
                age,
                table_no,
                waiter,
                category,
                item,
                quantity,
                unit_price,
                sales,
                discount,
                tax,
                total_bill,
                payment_method,
                order_type,
                rating,
                profit
            ))

            conn.commit()

            st.success("✅ Transaction Added Successfully!")

            st.balloons()

            st.rerun()

st.divider()

# ==========================================================
# View Transactions
# ==========================================================

st.header("📋 Sales Transactions")

sales_df = pd.read_sql(
    "SELECT * FROM sales ORDER BY Order_ID",
    conn
)

st.dataframe(
    sales_df,
    use_container_width=True,
    height=400
)

st.write(f"Total Transactions : {len(sales_df)}")

st.divider()

# ==========================================================
# Search Transaction
# ==========================================================

st.header("🔍 Search Transaction")

search_id = st.text_input(
    "Enter Order ID",
    placeholder="ORD1001"
)

if st.button("Search"):

    result = pd.read_sql(
        "SELECT * FROM sales WHERE Order_ID=?",
        conn,
        params=(search_id,)
    )

    if result.empty:

        st.error("No Transaction Found.")

    else:

        st.success("Transaction Found")

        st.dataframe(
            result,
            use_container_width=True
        )

st.divider()

# ==========================================================
# Update Transaction
# ==========================================================

st.header("✏ Update Transaction")

update_id = st.text_input(
    "Order ID to Update",
    placeholder="ORD1001"
)

new_quantity = st.number_input(
    "New Quantity",
    min_value=1,
    value=1
)

new_unit_price = st.number_input(
    "New Unit Price (£)",
    min_value=0.0,
    value=10.0
)

new_discount = st.number_input(
    "New Discount (£)",
    min_value=0.0,
    value=0.0
)

new_rating = st.slider(
    "New Rating",
    1,
    5,
    5,
    key="rating_update"
)

if st.button("Update Transaction"):

    sales = new_quantity * new_unit_price

    tax = sales * 0.05

    total_bill = sales - new_discount + tax

    profit = sales * 0.30

    cursor.execute("""

    UPDATE sales

    SET

    Quantity=?,

    Unit_Price=?,

    Sales=?,

    Discount=?,

    Tax=?,

    Total_Bill=?,

    Rating=?,

    Profit=?

    WHERE Order_ID=?

    """,

    (

        new_quantity,

        new_unit_price,

        sales,

        new_discount,

        tax,

        total_bill,

        new_rating,

        profit,

        update_id

    ))

    conn.commit()

    if cursor.rowcount == 0:

        st.warning("Order ID not found.")

    else:

        st.success("Transaction Updated Successfully.")

        st.rerun()

st.divider()

# ==========================================================
# Delete Transaction
# ==========================================================

st.header("🗑 Delete Transaction")

delete_id = st.text_input(
    "Order ID to Delete",
    placeholder="ORD1001"
)

if st.button("Delete Transaction"):

    cursor.execute(

        "DELETE FROM sales WHERE Order_ID=?",

        (delete_id,)

    )

    conn.commit()

    if cursor.rowcount == 0:

        st.warning("Order ID not found.")

    else:

        st.success("Transaction Deleted Successfully.")

        st.rerun()

st.divider()

# ==========================================================
# Download Transactions
# ==========================================================

st.header("📥 Download Transactions")

download_df = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

csv = download_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download Sales CSV",

    data=csv,

    file_name="Sales_Transactions.csv",

    mime="text/csv"

)

st.divider()

# ==========================================================
# Statistics
# ==========================================================

st.header("📊 Transaction Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    len(download_df)
)

col2.metric(
    "Revenue",
    f"£{download_df['Total_Bill'].sum():,.2f}"
)

col3.metric(
    "Average Bill",
    f"£{download_df['Total_Bill'].mean():,.2f}"
)

col4.metric(
    "Total Profit",
    f"£{download_df['Profit'].sum():,.2f}"
)

st.divider()

# ==========================================================
# Refresh
# ==========================================================

if st.button("🔄 Refresh Data"):

    st.rerun()

# ==========================================================
# Close Database
# ==========================================================

conn.close()