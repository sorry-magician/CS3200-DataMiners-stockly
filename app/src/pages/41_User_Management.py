import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('User Management')
st.write('---')

API_BASE = 'http://web-api:4000'

# ── Fetch all users
try:
    response = requests.get(f'{API_BASE}/users')
    users    = response.json()
except:
    st.error('Could not connect to the API.')
    users = []

# ── Current Users Table
st.subheader('Current Users')

if users:
    import pandas as pd
    df = pd.DataFrame(users, columns=[
        'User ID', 'Full Name', 'Email',
        'Role', 'Is Active', 'Created At'
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info('No users found.')

st.write('---')

# SECTION 1 — ADD A NEW USER
# User Story: Alex-1

st.subheader('Add a New User')

with st.form('add_user_form'):
    col1, col2 = st.columns(2)
    with col1:
        new_name  = st.text_input('Full Name')
        new_email = st.text_input('Email')
    with col2:
        new_role  = st.selectbox('Role', ['manager', 'editor', 'viewer', 'admin'])

    submitted = st.form_submit_button('Add User', use_container_width=True)

    if submitted:
        if not new_name or not new_email:
            st.error('Full name and email are required.')
        else:
            payload = {
                'full_name': new_name,
                'email':     new_email,
                'role':      new_role
            }
            try:
                r = requests.post(f'{API_BASE}/users', json=payload)
                if r.status_code == 201:
                    st.success(f'User {new_name} added successfully.')
                else:
                    st.error(f'Error: {r.text}')
            except:
                st.error('Could not connect to the API.')

st.write('---')


# SECTION 2 — UPDATE A USER
# User Story: Alex-5

st.subheader('Update User Information')

if users:
    user_options = {f"{u[1]} (ID: {u[0]})": u[0] for u in users}

    with st.form('update_user_form'):
        selected_user     = st.selectbox('Select User', list(user_options.keys()))
        updated_name      = st.text_input('New Full Name')
        updated_email     = st.text_input('New Email')
        updated_role      = st.selectbox('New Role',
                                         ['manager', 'editor', 'viewer', 'admin'])

        update_submitted  = st.form_submit_button('Update User',
                                                   use_container_width=True)

        if update_submitted:
            user_id = user_options[selected_user]
            payload = {
                'full_name': updated_name,
                'email':     updated_email,
                'role':      updated_role
            }
            try:
                r = requests.put(f'{API_BASE}/users/{user_id}', json=payload)
                if r.status_code == 200:
                    st.success('User updated successfully.')
                else:
                    st.error(f'Error: {r.text}')
            except:
                st.error('Could not connect to the API.')

st.write('---')


# SECTION 3 — DEACTIVATE A USER
# User Story: Alex-2

st.subheader('Deactivate a User Account')
st.write('Deactivating a user prevents them from accessing the system '
         'without deleting their account or activity history.')

if users:
    active_users = [u for u in users if u[4] == 1]
    if active_users:
        active_options = {f"{u[1]} (ID: {u[0]})": u[0] for u in active_users}

        with st.form('deactivate_user_form'):
            selected_deactivate = st.selectbox('Select User to Deactivate',
                                               list(active_options.keys()))
            deactivate_submitted = st.form_submit_button(
                'Deactivate User',
                type='primary',
                use_container_width=True
            )

            if deactivate_submitted:
                user_id = active_options[selected_deactivate]
                try:
                    r = requests.put(f'{API_BASE}/users/{user_id}/deactivate')
                    if r.status_code == 200:
                        st.success('User deactivated successfully.')
                    else:
                        st.error(f'Error: {r.text}')
                except:
                    st.error('Could not connect to the API.')
    else:
        st.info('No active users to deactivate.')