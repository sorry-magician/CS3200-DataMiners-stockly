import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('System Configuration')
st.write('---')

API_BASE = 'http://web-api:4000'

# ── Fetch current config ──
try:
    response = requests.get(f'{API_BASE}/system_config')
    config   = response.json()
except:
    st.error('Could not connect to the API.')
    config = []

# ── Display current config 
st.subheader('Current System Settings')

if config:
    df = pd.DataFrame(config, columns=[
        'Config Key', 'Config Value', 'Last Updated'
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info('No configuration settings found.')

st.write('---')


# SECTION 1 — UPDATE A CONFIG SETTING
# User Story: Alex-4

st.subheader('Update a Configuration Setting')

if config:
    config_keys    = [c[0] for c in config]
    config_options = {c[0]: c[1] for c in config}

    with st.form('update_config_form'):
        selected_key   = st.selectbox('Select Setting', config_keys)
        new_value      = st.text_input(
            'New Value',
            value=config_options.get(selected_key, '')
        )

        config_submitted = st.form_submit_button(
            'Update Setting',
            use_container_width=True
        )

        if config_submitted:
            if not new_value:
                st.error('Value cannot be empty.')
            else:
                payload = {'config_value': new_value}
                try:
                    r = requests.put(
                        f'{API_BASE}/system_config/{selected_key}',
                        json=payload
                    )
                    if r.status_code == 200:
                        st.success(f'{selected_key} updated to {new_value}.')
                    else:
                        st.error(f'Error: {r.text}')
                except:
                    st.error('Could not connect to the API.')

st.write('---')


# SECTION 2 — DELETE FLAGGED PRODUCT
# User Story: Alex-6

st.subheader('Delete Flagged Duplicate Products')
st.write('This permanently removes archived products that have been '
         'identified as duplicates. This action cannot be undone.')

with st.form('delete_flagged_form'):
    flagged_sku = st.text_input('Enter SKU of archived product to delete')

    delete_submitted = st.form_submit_button(
        'Permanently Delete Product',
        type='primary',
        use_container_width=True
    )

    if delete_submitted:
        if not flagged_sku:
            st.error('Please enter a SKU.')
        else:
            try:
                r = requests.delete(
                    f'{API_BASE}/products/{flagged_sku}/flag'
                )
                if r.status_code == 200:
                    st.success(f'Product {flagged_sku} permanently deleted.')
                else:
                    st.error(f'Error: {r.text}')
            except:
                st.error('Could not connect to the API.')