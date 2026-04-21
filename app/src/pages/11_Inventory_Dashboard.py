import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Inventory Dashboard')
st.write('---')

API_BASE = 'http://web-api:4000'

# ── Fetch all products
try:
    response = requests.get(f'{API_BASE}/products')
    products = response.json()
except:
    st.error('Could not connect to the API.')
    products = []

# ── KPI Cards
if products:
    total_skus        = len(products)
    total_value       = sum(float(p[3]) * int(p[4]) for p in products)
    low_stock_count   = sum(1 for p in products if int(p[4]) < int(p[5]))
    out_of_stock_count = sum(1 for p in products if int(p[4]) == 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total SKUs',         total_skus)
    col2.metric('Inventory Value',    f'${total_value:,.2f}')
    col3.metric('Low Stock Items',    low_stock_count)
    col4.metric('Out of Stock Items', out_of_stock_count)

st.write('---')

# ── Full Product Table
st.subheader('All Active Products')

if products:
    import pandas as pd
    df = pd.DataFrame(products, columns=[
        'SKU', 'Product Name', 'Description',
        'Unit Price', 'Qty on Hand', 'Reorder Threshold',
        'Is Archived', 'Category'
    ])
    st.dataframe(df[[
        'SKU', 'Product Name', 'Category',
        'Unit Price', 'Qty on Hand', 'Reorder Threshold'
    ]], use_container_width=True)
else:
    st.info('No products found.')

st.write('---')

# ── Low Stock Alerts
st.subheader('Low Stock Alerts')

try:
    ls_response = requests.get(f'{API_BASE}/products/low-stock')
    low_stock = ls_response.json()
except:
    low_stock = []

if low_stock:
    ls_df = pd.DataFrame(low_stock, columns=[
        'SKU', 'Product Name', 'Category',
        'Qty on Hand', 'Reorder Threshold', 'Units Needed'
    ])
    st.dataframe(ls_df, use_container_width=True)
else:
    st.success('All products are sufficiently stocked.')