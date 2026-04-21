# 30_Analyst_Home.py
# Landing page for Priya Nair — Business Analyst (Persona 3)
# Spencer | CS 3200 | Data Miners | Stockly

import streamlit as st

# ------------------------------------------------
# Guard: redirect to Home if no user is logged in
# ------------------------------------------------
if 'user' not in st.session_state:
    st.warning('Please log in from the Home page first.')
    st.stop()

user = st.session_state['user']

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title  = 'Analyst Home — Stockly',
    page_icon   = '📊',
    layout      = 'wide'
)

# ------------------------------------------------
# Header
# ------------------------------------------------
st.title(f'Welcome, {user["full_name"]} 👋')
st.subheader('Business Analyst Dashboard')
st.markdown('---')

st.markdown(
    '''
    Use the sidebar to navigate to your analytics tools.
    As a **Business Analyst**, you have access to:
    '''
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        '**📈 Revenue Dashboard**\n\n'
        'Track sales trends and revenue by category '
        'over any date range.'
    )

with col2:
    st.info(
        '**🏷️ Product Performance**\n\n'
        'View sell-through rates and inventory '
        'turnover ratios per SKU.'
    )

with col3:
    st.info(
        '**🚚 Supplier Analysis**\n\n'
        'Analyse supplier lead times and the stock '
        'they contribute to the catalog.'
    )

st.markdown('---')
st.caption(f'Logged in as: {user["email"]}  |  Role: {user["role"]}')
