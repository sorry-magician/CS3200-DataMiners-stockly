import logging
logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading Stockly Home page")

st.title('Stockly')
st.write('#### Welcome. Please select your role to continue.')
st.write('')

if st.button(
    'Maya Chen  —  Store Owner',
    type='primary',
    use_container_width=True
):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'store_owner'
    st.session_state['first_name'] = 'Maya'
    logger.info("Logging in as Store Owner")
    st.switch_page('pages/10_Store_Owner_Home.py')

if st.button(
    'Jordan Patel  —  Inventory Manager',
    type='primary',
    use_container_width=True
):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'inventory_manager'
    st.session_state['first_name'] = 'Jordan'
    logger.info("Logging in as Inventory Manager")
    st.switch_page('pages/20_Inventory_Manager_Home.py')

if st.button(
    'Priya Nair  —  Business Analyst',
    type='primary',
    use_container_width=True
):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['first_name'] = 'Priya'
    logger.info("Logging in as Business Analyst")
    st.switch_page('pages/30_Analyst_Home.py')

if st.button(
    'Alex Torres  —  System Administrator',
    type='primary',
    use_container_width=True
):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Alex'
    logger.info("Logging in as System Administrator")
    st.switch_page('pages/40_Admin_Home.py')