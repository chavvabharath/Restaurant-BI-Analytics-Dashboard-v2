import streamlit as st
import pandas as pd

st.title("Restaurant Dashboard Test")

df = pd.read_csv("data/restaurant_sales.csv")

st.success("CSV Loaded Successfully!")

st.write("Number of rows:", len(df))
st.write("Column Names:")
st.write(df.columns.tolist())

st.dataframe(df.head())