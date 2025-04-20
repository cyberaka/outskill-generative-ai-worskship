import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:9321"

st.title("📦 Product Inventory Manager")

menu = st.sidebar.selectbox("Choose Action", ["Add Product", "View All", "Search by ID", "Delete Product"])

if menu == "Add Product":
    st.header("➕ Add New Product")
    product_id = st.number_input("Product ID", min_value=1, step=1)
    name = st.text_input("Product Name")
    desc = st.text_input("Description")
    price = st.number_input("Price", min_value=0.0, step=0.01)
    qty = st.number_input("Quantity In Stock", min_value=0, step=1)

    if st.button("Add Product"):
        payload = {
            "product_id": product_id,
            "product_name": name,
            "product_description": desc,
            "product_price": price,
            "product_in_stock_qty": qty
        }
        res = requests.post(f"{API_BASE}/records/", json=payload)
        st.success(res.json().get("message", "Product added."))

elif menu == "View All":
    st.header("📋 All Products")
    res = requests.get(f"{API_BASE}/records")
    if res.ok:
        df = pd.DataFrame(res.json())
        st.dataframe(df)
    else:
        st.error("Failed to fetch products.")

elif menu == "Search by ID":
    st.header("🔍 Search Product by ID")
    record_id = st.number_input("Enter Product ID", min_value=1, step=1)
    if st.button("Search"):
        res = requests.get(f"{API_BASE}/records/{record_id}")
        if res.ok and res.json():
            st.json(res.json())
        else:
            st.warning("Product not found.")

elif menu == "Delete Product":
    st.header("❌ Delete Product by ID")
    record_id = st.number_input("Enter Product ID", min_value=1, step=1)
    api_key = st.text_input("Enter API Key", type="password")
    if st.button("Delete"):
        res = requests.delete(f"{API_BASE}/record", params={"id": record_id, "api_key": api_key})
        st.success(res.json().get("message", "Operation completed."))
