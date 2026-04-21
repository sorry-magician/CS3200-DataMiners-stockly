import streamlit as st
import requests

st.set_page_config(page_title='Stock Management — Stockly', layout='wide')

API_BASE = 'http://api:4000'

if 'user' not in st.session_state:
    st.warning('Please log in from the Home page first.')
    st.stop()

user_email = st.session_state['user'].get('email', 'jordan@stockly.com')

st.title('⚙️ Stock Management')
st.caption(
    'Log stock adjustments, update purchase order statuses, '
    'and deactivate inactive suppliers.'
)
st.divider()

# Three tabs — one per user story
tab1, tab2, tab3 = st.tabs([
    '📝 Log Stock Adjustment',
    '🔄 Update PO Status',
    '🗑️ Deactivate Supplier'
])

with tab1:
    st.subheader('Log a Manual Stock Adjustment')
    st.caption(
        'Record any quantity change with a documented reason. '
        'Use a negative number for stock that is being removed (e.g. damaged units).'
    )

    with st.form('stock_adj_form', clear_on_submit=True):
        col_left, col_right = st.columns(2)

        with col_left:
            sku             = st.text_input('Product SKU *', placeholder='APR-001')
            adjustment_type = st.selectbox(
                'Adjustment Type',
                ['damaged', 'correction']
            )

        with col_right:
            quantity_delta = st.number_input(
                'Quantity Change *',
                step=1,
                value=-1,
                help='Negative = stock removed, Positive = stock added'
            )
            reason = st.text_area(
                'Reason for Adjustment *',
                placeholder='e.g. Water damage found during storage check',
                height=100
            )

        adj_submitted = st.form_submit_button(
            'Save Adjustment', type='primary'
        )

    if adj_submitted:
        if not sku.strip():
            st.error('SKU is required.')
        elif not reason.strip():
            st.error('A reason is required for every adjustment.')
        else:
            payload = {
                'sku':             sku.strip().upper(),
                'quantity_delta':  int(quantity_delta),
                'adjustment_type': adjustment_type,
                'reason':          reason.strip(),
                'user_email':      user_email
            }
            try:
                resp = requests.post(
                    f'{API_BASE}/api/stock_adjustments', json=payload
                )
                if resp.status_code == 201:
                    st.success(
                        f'Stock adjustment logged for **{sku.strip().upper()}**. '
                        f'Verify in DataGrip: '
                        f'`SELECT * FROM Stock_Adjustments ORDER BY adjustment_id DESC LIMIT 5;`'
                    )
                else:
                    st.error(
                        f'Failed to log adjustment. '
                        f'Ensure the SKU exists in the Products table. '
                        f'(HTTP {resp.status_code})'
                    )
            except Exception as e:
                st.error(f'API connection error: {e}')


with tab1:
    st.subheader('Log a Manual Stock Adjustment')
    st.caption(
        'Record any quantity change with a documented reason. '
        'Use a negative number for stock that is being removed (e.g. damaged units).'
    )

    with st.form('stock_adj_form', clear_on_submit=True):
        col_left, col_right = st.columns(2)

        with col_left:
            sku             = st.text_input('Product SKU *', placeholder='APR-001')
            adjustment_type = st.selectbox(
                'Adjustment Type',
                ['damaged', 'correction']
            )

        with col_right:
            quantity_delta = st.number_input(
                'Quantity Change *',
                step=1,
                value=-1,
                help='Negative = stock removed, Positive = stock added'
            )
            reason = st.text_area(
                'Reason for Adjustment *',
                placeholder='e.g. Water damage found during storage check',
                height=100
            )

        adj_submitted = st.form_submit_button(
            'Save Adjustment', type='primary'
        )

    if adj_submitted:
        if not sku.strip():
            st.error('SKU is required.')
        elif not reason.strip():
            st.error('A reason is required for every adjustment.')
        else:
            payload = {
                'sku':             sku.strip().upper(),
                'quantity_delta':  int(quantity_delta),
                'adjustment_type': adjustment_type,
                'reason':          reason.strip(),
                'user_email':      user_email
            }
            try:
                resp = requests.post(
                    f'{API_BASE}/api/stock_adjustments', json=payload
                )
                if resp.status_code == 201:
                    st.success(
                        f'Stock adjustment logged for **{sku.strip().upper()}**. '
                        f'Verify in DataGrip: '
                        f'`SELECT * FROM Stock_Adjustments ORDER BY adjustment_id DESC LIMIT 5;`'
                    )
                else:
                    st.error(
                        f'Failed to log adjustment. '
                        f'Ensure the SKU exists in the Products table. '
                        f'(HTTP {resp.status_code})'
                    )
            except Exception as e:
                st.error(f'API connection error: {e}')

with tab2:
    st.subheader('Update Purchase Order Status')
    st.caption(
        'Move a PO through its lifecycle: '
        '**ordered** → **in_transit** → **received**.'
    )

    with st.form('update_po_form', clear_on_submit=False):
        po_col, status_col = st.columns(2)

        with po_col:
            po_id = st.number_input(
                'Purchase Order ID *', min_value=1, step=1, value=1
            )

        with status_col:
            new_status = st.selectbox(
                'New Status',
                ['ordered', 'in_transit', 'received']
            )

        po_submitted = st.form_submit_button('Update Status', type='primary')

    if po_submitted:
        try:
            resp = requests.put(
                f'{API_BASE}/api/purchase_orders/{int(po_id)}',
                json={'status': new_status}
            )
            if resp.status_code == 200:
                st.success(
                    f'PO **{int(po_id)}** status updated to **{new_status}**. '
                    f'Verify in DataGrip: '
                    f'`SELECT status FROM Purchase_Orders WHERE po_id = {int(po_id)};`'
                )
            else:
                st.error(
                    f'Failed to update PO {int(po_id)}. '
                    f'Check that the PO ID exists. '
                    f'(HTTP {resp.status_code})'
                )
        except Exception as e:
            st.error(f'API connection error: {e}')
with tab3:
    st.subheader('Deactivate a Supplier')
    st.caption(
        'Mark a vendor as inactive when you stop working with them. '
        'The supplier record is kept for historical purchase order data — '
        'it simply disappears from active supplier lists.'
    )


    try:
        sup_resp  = requests.get(f'{API_BASE}/api/suppliers')
        suppliers = sup_resp.json() if sup_resp.status_code == 200 else []
    except Exception:
        suppliers = []

    if not suppliers:
        st.warning('No active suppliers found or the API is unreachable.')
    else:
        sup_map = {s['supplier_name']: s['supplier_id'] for s in suppliers}

        with st.form('deactivate_supplier_form', clear_on_submit=False):
            selected_name = st.selectbox(
                'Select Supplier to Deactivate',
                list(sup_map.keys())
            )
            confirm = st.checkbox(
                f'I confirm I want to deactivate this supplier. '
                f'This cannot be undone from the UI.'
            )
            del_submitted = st.form_submit_button(
                'Deactivate Supplier', type='primary'
            )

        if del_submitted:
            if not confirm:
                st.error(
                    'Please check the confirmation box before proceeding.'
                )
            else:
                supplier_id = sup_map[selected_name]
                try:
                    resp = requests.delete(
                        f'{API_BASE}/api/suppliers/{supplier_id}'
                    )
                    if resp.status_code == 200:
                        st.success(
                            f'Supplier **"{selected_name}"** has been deactivated. '
                            f'Verify in DataGrip: '
                            f'`SELECT is_active FROM Suppliers WHERE supplier_id = {supplier_id};`'
                        )
                    else:
                        st.error(
                            f'Failed to deactivate supplier. '
                            f'(HTTP {resp.status_code})'
                        )
                except Exception as e:
                    st.error(f'API connection error: {e}')
