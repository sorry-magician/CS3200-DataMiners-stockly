import streamlit as st
import requests

st.set_page_config(page_title='Inventory Search — Stockly', layout='wide')

API_BASE = 'http://web-api:4000'

if 'user' not in st.session_state:
    st.warning('Please log in from the Home page first.')
    st.stop()

st.title('🔍 Inventory Search & Filter')
st.caption(
    'Use the sidebar filters to narrow down the product catalog '
    'by category and/or supplier. Leave both set to "All" to see the full catalog.'
)
st.divider()

try:
    cat_resp   = requests.get(f'{API_BASE}/api/categories')
    categories = cat_resp.json() if cat_resp.status_code == 200 else []
except Exception:
    categories = []

try:
    sup_resp  = requests.get(f'{API_BASE}/api/suppliers')
    suppliers = sup_resp.json() if sup_resp.status_code == 200 else []
except Exception:
    suppliers = []

cat_options = {'All': None}
cat_options.update(
    {c['category_name']: c['category_id'] for c in categories}
)

sup_options = {'All': None}
sup_options.update(
    {s['supplier_name']: s['supplier_id'] for s in suppliers}
)

with st.sidebar:
    st.header('🔧 Filters')
    st.caption('Select one or both filters, then click Apply.')

    selected_cat_name = st.selectbox('Category', list(cat_options.keys()))
    selected_sup_name = st.selectbox('Supplier',  list(sup_options.keys()))

    apply_btn = st.button('Apply Filters', type='primary', use_container_width=True)
    clear_btn = st.button('Clear Filters', use_container_width=True)

if clear_btn:
    st.info('Filters cleared. Select new filters and click Apply.')

elif apply_btn:
    params     = {}
    cat_id     = cat_options[selected_cat_name]
    sup_id     = sup_options[selected_sup_name]

    if cat_id is not None:
        params['category_id'] = cat_id
    if sup_id is not None:
        params['supplier_id'] = sup_id

    filter_desc_parts = []
    if selected_cat_name != 'All':
        filter_desc_parts.append(f'Category: **{selected_cat_name}**')
    if selected_sup_name != 'All':
        filter_desc_parts.append(f'Supplier: **{selected_sup_name}**')

    if filter_desc_parts:
        st.markdown('Active filters: ' + ' | '.join(filter_desc_parts))
    else:
        st.markdown('Showing **all active products** (no filters applied).')

    try:
        search_resp = requests.get(
            f'{API_BASE}/api/inventory/search', params=params
        )
        if search_resp.status_code == 200:
            results = search_resp.json()

            st.subheader(f'Results — {len(results)} product(s) found')

            if results:
                # Highlight low-stock rows so Jordan can spot them easily
                st.dataframe(results, use_container_width=True)

                # Quick summary metrics below the table
                low_stock_count = sum(
                    1 for r in results
                    if r.get('quantity_on_hand', 0) < r.get('reorder_threshold', 0)
                )
                out_of_stock_count = sum(
                    1 for r in results
                    if r.get('quantity_on_hand', 0) == 0
                )

                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric('Total Products', len(results))
                m2.metric('Low Stock',      low_stock_count)
                m3.metric('Out of Stock',   out_of_stock_count)
            else:
                st.info('No products match the selected filters.')

        else:
            st.error(
                f'Search request failed. (HTTP {search_resp.status_code})'
            )

    except Exception as e:
        st.error(f'API connection error: {e}')

else:
    st.info(
        'Select a Category and/or Supplier in the sidebar, '
        'then click **Apply Filters** to see matching products.'
    )