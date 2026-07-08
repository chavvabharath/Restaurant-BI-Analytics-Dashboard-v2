import streamlit as st
import pandas as pd

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(page_title="Reports", layout="wide")

st.title("📄 Reports")
st.markdown("Generate and download restaurant reports.")

# -------------------------------------------------------
# Load Datasets
# -------------------------------------------------------
import sqlite3
import pandas as pd

conn = sqlite3.connect("database/restaurant.db")

sales = pd.read_csv("data/restaurant_sales.csv")
expenses = pd.read_csv("data/expenses.csv")
inventory = pd.read_csv("data/inventory.csv")
employees = pd.read_csv("data/employees.csv")

sales.to_sql("sales", conn, if_exists="replace", index=False)
expenses.to_sql("expenses", conn, if_exists="replace", index=False)
inventory.to_sql("inventory", conn, if_exists="replace", index=False)
employees.to_sql("employees", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database Created Successfully")

# -------------------------------------------------------
# Dataset Selection
# -------------------------------------------------------
dataset = st.selectbox(
    "📂 Select Dataset",
    (
        "Sales",
        "Inventory",
        "Employees",
        "Expenses"
    )
)

# -------------------------------------------------------
# Choose Dataset
# -------------------------------------------------------
if dataset == "Sales":
    df = sales
    filename = "sales_report.csv"

elif dataset == "Inventory":
    df = inventory
    filename = "inventory_report.csv"

elif dataset == "Employees":
    df = employees
    filename = "employees_report.csv"

else:
    df = expenses
    filename = "expenses_report.csv"

# -------------------------------------------------------
# Dataset Information
# -------------------------------------------------------
st.subheader("📊 Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

# -------------------------------------------------------
# Preview Dataset
# -------------------------------------------------------
st.subheader("👀 Preview of Dataset")

st.dataframe(df, use_container_width=True)

# -------------------------------------------------------
# Download Button
# -------------------------------------------------------
st.subheader("⬇ Download Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label=f"Download {dataset} Report",
    data=csv,
    file_name=filename,
    mime="text/csv"
)

# -------------------------------------------------------
# Summary Statistics
# -------------------------------------------------------
st.subheader("📈 Summary Statistics")

try:
    st.dataframe(df.describe(include="all"), use_container_width=True)
except:
    st.dataframe(df.describe(), use_container_width=True)

# -------------------------------------------------------
# Missing Values
# -------------------------------------------------------
st.subheader("❗ Missing Values")

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

st.dataframe(missing, use_container_width=True)

# -------------------------------------------------------
# Data Types
# -------------------------------------------------------
st.subheader("📝 Data Types")

datatype = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values
})

st.dataframe(datatype, use_container_width=True)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.success("✅ Report generated successfully.")