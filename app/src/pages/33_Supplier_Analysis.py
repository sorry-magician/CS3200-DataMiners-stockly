import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(page_title='Supplier Analysis — Stockly', page_icon='🚚', layout='wide')
SideBarLinks()

if not st.session_state.get('authenticated'):
    st.warning('Please log in from the Home page first.')
    st.stop()

API_BASE = 'http://api:4000/api'

st.title('🚚 Supplier Lead Time Analysis')
st.markdown('Compare lead times across active suppliers and see how much of the catalog each one contributes.')
st.markdown('---')

if st.button('Load Supplier Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/supplier_lead_times')
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df['lead_time_days'] = pd.to_numeric(df['lead_time_days'])
                df['products_supplied'] = pd.to_numeric(df['products_supplied'])
                df['total_stock_supplied'] = pd.to_numeric(df['total_stock_supplied'])
                df['avg_stock_per_product'] = pd.to_numeric(df['avg_stock_per_product'])

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric('Active Suppliers', len(df))
                with c2:
                    st.metric('Avg Lead Time', f'{df["lead_time_days"].mean():.1f} days')
                with c3:
                    fastest = df.loc[df['lead_time_days'].idxmin(), 'supplier_name']
                    st.metric('Fastest Supplier', fastest)

                st.markdown('#### Lead Time by Supplier (days)')
                st.bar_chart(df.set_index('supplier_name')[['lead_time_days']])

                st.markdown('#### Total Stock Supplied per Supplier')
                st.bar_chart(df.set_index('supplier_name')[['total_stock_supplied']])

                threshold = df['lead_time_days'].quantile(0.75)
                slow = df[df['lead_time_days'] >= threshold]
                if not slow.empty:
                    st.markdown(f'#### ⚠️ Slower Suppliers (≥ {threshold:.0f} days lead time)')
                    st.dataframe(slow[['supplier_name','lead_time_days','products_supplied','total_stock_supplied']].rename(columns={
                        'supplier_name': 'Supplier',
                        'lead_time_days': 'Lead Time (days)',
                        'products_supplied': 'Products Supplied',
                        'total_stock_supplied': 'Total Units Supplied'
                    }), use_container_width=True)

                st.markdown('#### Full Supplier Overview')
                display_df = df[['supplier_name','lead_time_days','products_supplied','total_stock_supplied','avg_stock_per_product']].copy()
                display_df['avg_stock_per_product'] = display_df['avg_stock_per_product'].map('{:.1f}'.format)
                display_df.columns = ['Supplier','Lead Time (days)','Products Supplied','Total Units Supplied','Avg Units per Product']
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info('No active supplier data found.')
        else:
            st.error(f'API error {response.status_code}: {response.text}')
    except Exception as e:
        st.error(f'Could not connect to the API: {e}')
