import streamlit as st
import requests
from datetime import date, timedelta

st.set_page_config(page_title='Purchase Orders — Stockly', layout='wide')

API_BASE = 'http://web-api:4000'

if 'user' not in st.session_state:
    st.warning('Please log in from the Home page first.')
    st.stop()

user_email = st.session_state['user'].get('email', 'jordan@stockly.com')

st.title('📦 Purchase Orders')
st.caption('Create new purchase orders and track supplier deliveries.')
st.divider()

st.subheader('All Purchase Orders')

col_filter, col_spacer = st.columns([2, 6])
with col_filter:
    status_filter = st.selectbox(
        'Filter by Status',
        ['All', 'ordered', 'in_transit', 'received'],
        key='po_status_filter'
    )

try:
    resp = requests.get(f'{API_BASE}/api/purchase_orders')
    if resp.status_code == 200:
        pos = resp.json()
        if status_filter != 'All':
            pos = [po for po in pos if po['status'] == status_filter]
        if pos:
            st.dataframe(pos, use_container_width=True)
        else:
            st.info('No purchase orders match the selected filter.')
    else:
        st.error(f'Could not load purchase orders. (HTTP {resp.status_code})')
except Exception as e:
    st.error(f'API connection error: {e}')

st.divider()

st.subheader('View PO Detail & Line Items')
st.caption('Enter a PO ID to see the full order breakdown including products, quantities, and lead time.')

detail_col, btn_col = st.columns([3, 1])
with detail_col:
    po_id_input = st.number_input(
        'PO ID', min_value=1, step=1, value=1, key='detail_po_id'
    )
with btn_col:
    st.write('')  # vertical alignment spacer
    st.write('')
    load_btn = st.button('Load Detail')

if load_btn:
    try:
        detail_resp = requests.get(
            f'{API_BASE}/api/purchase_orders/{int(po_id_input)}'
        )
        if detail_resp.status_code == 200:
            detail = detail_resp.json()
            if detail:
                st.dataframe(detail, use_container_width=True)
            else:
                st.warning(f'No purchase order found with ID {int(po_id_input)}.')
        else:
            st.error(f'Could not load PO detail. (HTTP {detail_resp.status_code})')
    except Exception as e:
        st.error(f'API connection error: {e}')

st.divider()

st.subheader('Create New Purchase Order')
st.caption('Select a supplier, set the expected delivery date, and add at least one product line item.')

# Load active suppliers for the dropdown
try:
    sup_resp  = requests.get(f'{API_BASE}/api/suppliers')
    suppliers = sup_resp.json() if sup_resp.status_code == 200 else []
except Exception:
    suppliers = []

if not suppliers:
    st.warning('Could not load suppliers from the API. Check that the Flask server is running.')
    st.stop()

supplier_names = [s['supplier_name'] for s in suppliers]

with st.form('create_po_form', clear_on_submit=True):
    st.markdown('**Order Header**')
    header_col1, header_col2 = st.columns(2)

    with header_col1:
        selected_supplier = st.selectbox('Supplier', supplier_names)
        expected_date = st.date_input(
            'Expected Delivery Date',
            value=date.today() + timedelta(days=14),
            min_value=date.today()
        )

    with header_col2:
        notes = st.text_area('Notes (optional)', height=100)

    st.markdown('**Product Line Items** — add at least one SKU')
    item_col1, item_col2, item_col3, item_col4 = st.columns(4)

    with item_col1:
        sku1 = st.text_input('SKU 1 *', placeholder='APR-001')
        qty1 = st.number_input('Qty 1', min_value=1, value=1, step=1)

    with item_col2:
        sku2 = st.text_input('SKU 2', placeholder='optional')
        qty2 = st.number_input('Qty 2', min_value=1, value=1, step=1)

    with item_col3:
        sku3 = st.text_input('SKU 3', placeholder='optional')
        qty3 = st.number_input('Qty 3', min_value=1, value=1, step=1)

    with item_col4:
        sku4 = st.text_input('SKU 4', placeholder='optional')
        qty4 = st.number_input('Qty 4', min_value=1, value=1, step=1)

    submitted = st.form_submit_button('Create Purchase Order', type='primary')

if submitted:
    if not sku1.strip():
        st.error('At least one SKU is required.')
    else:
        # Build items list — only include rows where the SKU was filled in
        items = [{'sku': sku1.strip(), 'quantity_ordered': int(qty1)}]
        if sku2.strip():
            items.append({'sku': sku2.strip(), 'quantity_ordered': int(qty2)})
        if sku3.strip():
            items.append({'sku': sku3.strip(), 'quantity_ordered': int(qty3)})
        if sku4.strip():
            items.append({'sku': sku4.strip(), 'quantity_ordered': int(qty4)})

        payload = {
            'supplier_name':          selected_supplier,
            'expected_delivery_date': str(expected_date),
            'notes':                  notes,
            'user_email':             user_email,
            'items':                  items
        }

        try:
            create_resp = requests.post(
                f'{API_BASE}/api/purchase_orders', json=payload
            )
            if create_resp.status_code == 201:
                new_id = create_resp.json().get('po_id')
                st.success(
                    f'Purchase order created successfully! '
                    f'New PO ID: **{new_id}** — verify in DataGrip with: '
                    f'`SELECT * FROM Purchase_Orders WHERE po_id = {new_id};`'
                )
            else:
                st.error(
                    f'Failed to create purchase order. '
                    f'Ensure all SKUs exist in the Products table. '
                    f'(HTTP {create_resp.status_code})'
                )
        except Exception as e:
            st.error(f'API connection error: {e}')