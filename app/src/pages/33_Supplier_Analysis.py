# 33_Supplier_Analysis.py
# Supplier lead time and stock contribution analysis
# Serves Priya Nair — Business Analyst (Persona 3)
# User Story: Priya-6
# Spencer | CS 3200 | Data Miners | Stockly

import streamlit as st
import requests
import pandas as pd

# ------------------------------------------------
# Guard: redirect to Home if no user is logged in
# ------------------------------------------------
if 'user' not in st.session_state:
    st.warning('Please log in from the Home page first.')
    st.stop()

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title = 'Supplier Analysis — Stockly',
    page_icon  = '🚚',
    layout     = 'wide'
)

API_BASE = 'http://api:4000/api'

# ------------------------------------------------
# Page header
# ------------------------------------------------
st.title('🚚 Supplier Lead Time Analysis')
st.markdown(
    'Compare lead times across active suppliers and see '
    'how much of the catalog each one contributes.'
)
st.markdown('---')

# ------------------------------------------------
# SECTION — Supplier Lead Times (Priya-6)
# Calls GET /analytics/supplier_lead_times
# ------------------------------------------------

if st.button('Load Supplier Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/supplier_lead_times')

        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)

                # KPI cards
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric('Active Suppliers', len(df))
                with c2:
                    avg_lead = df['lead_time_days'].mean()
                    st.metric('Avg Lead Time', f'{avg_lead:.1f} days')
                with c3:
                    fastest = df.loc[
                        df['lead_time_days'].idxmin(), 'supplier_name'
                    ]
                    st.metric('Fastest Supplier', fastest)

                # Lead time bar chart
                st.markdown('#### Lead Time by Supplier (days)')
                lead_chart = df.set_index('supplier_name')[['lead_time_days']]
                st.bar_chart(lead_chart)

                # Stock contribution bar chart
                st.markdown('#### Total Stock Supplied per Supplier')
                stock_chart = df.set_index('supplier_name')[
                    ['total_stock_supplied']
                ]
                st.bar_chart(stock_chart)

                # Highlight suppliers with long lead times
                threshold = df['lead_time_days'].quantile(0.75)
                slow_suppliers = df[df['lead_time_days'] >= threshold]

                if not slow_suppliers.empty:
                    st.markdown('#### ⚠️ Suppliers with Longer Lead Times')
                    st.caption(
                        f'Suppliers in the top 25% of lead times '
                        f'(≥ {threshold:.0f} days)'
                    )
                    st.dataframe(
                        slow_suppliers[[
                            'supplier_name', 'lead_time_days',
                            'products_supplied', 'total_stock_supplied'
                        ]].rename(columns={
                            'supplier_name'      : 'Supplier',
                            'lead_time_days'     : 'Lead Time (days)',
                            'products_supplied'  : 'Products Supplied',
                            'total_stock_supplied': 'Total Units Supplied'
                        }),
                        use_container_width=True
                    )

                # Full table
                st.markdown('#### Full Supplier Overview')
                display_df = df[[
                    'supplier_name', 'lead_time_days',
                    'products_supplied',
                    'total_stock_supplied', 'avg_stock_per_product'
                ]].copy()
                display_df['avg_stock_per_product'] = display_df[
                    'avg_stock_per_product'
                ].map('{:.1f}'.format)
                display_df.columns = [
                    'Supplier', 'Lead Time (days)', 'Products Supplied',
                    'Total Units Supplied', 'Avg Units per Product'
                ]
                st.dataframe(display_df, use_container_width=True)

            else:
                st.info('No active supplier data found.')

        else:
            st.error(f'API error {response.status_code}: {response.text}')

    except Exception as e:
        st.error(f'Could not connect to the API: {e}')
