import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Audit Log')
st.write('---')
st.write('View a complete history of all changes made to the system.')

API_BASE = 'http://localhost:4000'

# ── Filters 
col1, col2 = st.columns(2)

with col1:
    table_filter = st.selectbox(
        'Filter by Table',
        ['All', 'Products', 'Users', 'Stock_Adjustments',
         'Purchase_Orders', 'System_Config']
    )

with col2:
    flagged_filter = st.selectbox(
        'Filter by Flagged Status',
        ['All', 'Flagged Only', 'Not Flagged']
    )

st.write('')

# ── Build query params
params = {}

if table_filter != 'All':
    params['table_name'] = table_filter

if flagged_filter == 'Flagged Only':
    params['is_flagged'] = 1
elif flagged_filter == 'Not Flagged':
    params['is_flagged'] = 0

# ── Fetch audit log
try:
    response  = requests.get(f'{API_BASE}/audit_log', params=params)
    audit_log = response.json()
except:
    st.error('Could not connect to the API.')
    audit_log = []

# ── Display results
if audit_log:
    df = pd.DataFrame(audit_log, columns=[
        'Log ID', 'Action Type', 'Table Name',
        'Record Ref', 'Changed At', 'Is Flagged', 'Changed By'
    ])

    st.metric('Total Log Entries', len(df))
    flagged_count = df['Is Flagged'].sum()
    st.metric('Flagged Entries', int(flagged_count))

    st.write('---')
    st.dataframe(df, use_container_width=True)
else:
    st.info('No audit log entries found for the selected filters.')