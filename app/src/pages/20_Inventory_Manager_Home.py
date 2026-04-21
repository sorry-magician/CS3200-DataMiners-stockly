import streamlit as st

from modules.nav import SideBarLinks
SideBarLinks()

st.set_page_config(page_title='Inventory Manager — Stockly', layout='wide')

if not st.session_state.get('authenticated'):
    st.warning('Please log in from the Home page first.')
    st.stop()

st.title('📦 Inventory Manager Portal')
st.subheader(f'Welcome, {st.session_state.get("first_name", "Jordan")}')
st.caption('Manage purchase orders, track stock levels, and maintain supplier records.')
st.divider()

st.markdown('''
### Your Pages
 
- **Purchase Orders** — Create new POs and view reorder history
- **Inventory Search** — Filter products by category and supplier  
- **Stock Management** — Log adjustments, update PO status, deactivate suppliers
''')
