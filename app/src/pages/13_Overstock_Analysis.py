import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Overstock Analysis')
st.write('---')
st.write('Products with high inventory but low sales in the last 90 days.')

API_BASE = 'http://web-api:4000'

try:
    response  = requests.get(f'{API_BASE}/products/overstock')
    overstock = response.json()
except:
    st.error('Could not connect to the API.')
    overstock = []

if overstock:
    df = pd.DataFrame(overstock, columns=[
        'SKU', 'Product Name',
        'Qty on Hand', 'Reorder Threshold',
        'Units Sold (Last 90 Days)'
    ])

    st.metric('Overstocked Products', len(df))
    st.write('---')
    st.dataframe(df, use_container_width=True)

    st.write('---')
    st.write('**What this means:** These products have more stock than their '
             'reorder threshold suggests is needed, and have sold fewer units '
             'than their threshold in the last 90 days. Consider running '
             'promotions or reducing future order quantities.')
else:
    st.success('No overstocked products detected based on recent sales data.')
    st.write('This could mean Spencer has not yet committed sales data. '
             'Once sales data is loaded this page will populate automatically.')