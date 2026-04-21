import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(
    page_title = 'Analyst Home — Stockly',
    page_icon  = '📊',
    layout     = 'wide'
)

SideBarLinks()

# Guard
if not st.session_state.get('authenticated'):
    st.warning('Please log in from the Home page first.')
    st.stop()

st.title(f'Welcome, {st.session_state.get("first_name", "Priya")} 👋')
st.subheader('Business Analyst Dashboard')
st.markdown('---')

st.markdown('Use the sidebar to navigate to your analytics tools. As a **Business Analyst**, you have access to:')

col1, col2, col3 = st.columns(3)

with col1:
    st.info('**📈 Revenue Dashboard**\n\nTrack sales trends and revenue by category over any date range.')

with col2:
    st.info('**🏷️ Product Performance**\n\nView sell-through rates and inventory turnover ratios per SKU.')

with col3:
    st.info('**🚚 Supplier Analysis**\n\nAnalyse supplier lead times and the stock they contribute to the catalog.')
