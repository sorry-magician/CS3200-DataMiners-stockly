import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Maya')}!")
st.write('### Store Owner Dashboard')
st.write('---')
st.write('Use the sidebar to navigate to your tools.')

col1, col2, col3 = st.columns(3)

with col1:
    st.info('**Inventory Dashboard**\n\nView stock levels, KPIs, and low-stock alerts.')
    if st.button('Go to Inventory Dashboard', use_container_width=True):
        st.switch_page('pages/11_Inventory_Dashboard.py')

with col2:
    st.info('**Product Management**\n\nAdd, update, or archive products in your catalog.')
    if st.button('Go to Product Management', use_container_width=True):
        st.switch_page('pages/12_Product_Management.py')

with col3:
    st.info('**Overstock Analysis**\n\nIdentify overstocked products using sales history.')
    if st.button('Go to Overstock Analysis', use_container_width=True):
        st.switch_page('pages/13_Overstock_Analysis.py')