import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Alex')}!")
st.write('### System Administrator Dashboard')
st.write('---')
st.write('Use the sidebar to navigate to your admin tools.')

col1, col2, col3 = st.columns(3)

with col1:
    st.info('**User Management**\n\nAdd, update, and deactivate user accounts.')
    if st.button('Go to User Management', use_container_width=True):
        st.switch_page('pages/41_User_Management.py')

with col2:
    st.info('**Audit Log**\n\nView a history of all changes made to the system.')
    if st.button('Go to Audit Log', use_container_width=True):
        st.switch_page('pages/42_Audit_Log.py')

with col3:
    st.info('**System Config**\n\nConfigure system-wide settings and manage flagged products.')
    if st.button('Go to System Config', use_container_width=True):
        st.switch_page('pages/43_System_Config.py')