import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Product Management')
st.write('---')

API_BASE = 'http://web-api:4000'

# ── Fetch categories for dropdowns
try:
    cat_response = requests.get(f'{API_BASE}/categories')
    categories   = cat_response.json()
    cat_names    = [c[1] for c in categories]
except:
    categories = []
    cat_names  = []

# ── Fetch products for dropdowns
try:
    prod_response = requests.get(f'{API_BASE}/products')
    products      = prod_response.json()
    skus          = [p[0] for p in products]
except:
    products = []
    skus     = []

# SECTION 1 — ADD A NEW PRODUCT
# User Story: Maya-2

st.subheader('Add a New Product')

with st.form('add_product_form'):
    col1, col2 = st.columns(2)
    with col1:
        new_sku          = st.text_input('SKU')
        new_name         = st.text_input('Product Name')
        new_description  = st.text_area('Description')
        new_category     = st.selectbox('Category', cat_names)
    with col2:
        new_price        = st.number_input('Unit Price ($)', min_value=0.01, step=0.01)
        new_qty          = st.number_input('Quantity on Hand', min_value=0, step=1)
        new_threshold    = st.number_input('Reorder Threshold', min_value=1, step=1)

    submitted = st.form_submit_button('Add Product', use_container_width=True)

    if submitted:
        if not new_sku or not new_name:
            st.error('SKU and Product Name are required.')
        else:
            payload = {
                'sku':               new_sku,
                'product_name':      new_name,
                'description':       new_description,
                'unit_price':        new_price,
                'quantity_on_hand':  new_qty,
                'reorder_threshold': new_threshold,
                'category_name':     new_category
            }
            try:
                r = requests.post(f'{API_BASE}/products', json=payload)
                if r.status_code == 201:
                    st.success(f'Product {new_sku} added successfully.')
                else:
                    st.error(f'Error: {r.text}')
            except:
                st.error('Could not connect to the API.')

st.write('---')

# SECTION 2 — UPDATE A PRODUCT
# User Story: Maya-4

st.subheader('Update Product Price and Reorder Threshold')

with st.form('update_product_form'):
    selected_sku      = st.selectbox('Select SKU to Update', skus)
    updated_price     = st.number_input('New Unit Price ($)',
                                        min_value=0.01, step=0.01)
    updated_threshold = st.number_input('New Reorder Threshold',
                                        min_value=1, step=1)

    update_submitted = st.form_submit_button('Update Product',
                                             use_container_width=True)

    if update_submitted:
        payload = {
            'unit_price':        updated_price,
            'reorder_threshold': updated_threshold
        }
        try:
            r = requests.put(f'{API_BASE}/products/{selected_sku}',
                             json=payload)
            if r.status_code == 200:
                st.success(f'Product {selected_sku} updated successfully.')
            else:
                st.error(f'Error: {r.text}')
        except:
            st.error('Could not connect to the API.')

st.write('---')


# SECTION 3 — ARCHIVE A PRODUCT
# User Story: Maya-5

st.subheader('Archive a Discontinued Product')
st.write('Archiving removes a product from the active catalog without '
         'deleting its historical data.')

with st.form('archive_product_form'):
    archive_sku = st.selectbox('Select SKU to Archive', skus)

    archive_submitted = st.form_submit_button('Archive Product',
                                              type='primary',
                                              use_container_width=True)

    if archive_submitted:
        try:
            r = requests.delete(f'{API_BASE}/products/{archive_sku}')
            if r.status_code == 200:
                st.success(f'Product {archive_sku} has been archived.')
            else:
                st.error(f'Error: {r.text}')
        except:
            st.error('Could not connect to the API.')