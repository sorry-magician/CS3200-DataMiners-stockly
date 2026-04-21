# 31_Revenue_Dashboard.py
# Revenue trends and category performance dashboard
# Serves Priya Nair — Business Analyst (Persona 3)
# User Stories: Priya-1, Priya-2
# Spencer | CS 3200 | Data Miners | Stockly

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(page_title='Revenue Dashboard — Stockly', page_icon='📈', layout='wide')
SideBarLinks()

if not st.session_state.get('authenticated'):
    st.warning('Please log in from the Home page first.')
    st.stop()

API_BASE = 'http://api:4000/api'

st.title('📈 Revenue Dashboard')
st.markdown('Track daily revenue trends and compare performance across product categories.')
st.markdown('---')

# SECTION 1 — Revenue Trends (Priya-1)
st.subheader('Sales Revenue Trends')

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start Date', value=pd.Timestamp('2024-01-01'))
with col2:
    end_date = st.date_input('End Date', value=pd.Timestamp.today())

if st.button('Load Revenue Data', type='primary'):
    try:
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        response = requests.get(f'{API_BASE}/analytics/revenue', params=params)

        if response.status_code == 200:
            revenue_data = response.json()
            if revenue_data:
                df = pd.DataFrame(revenue_data)
                df['order_date'] = pd.to_datetime(df['order_date'])
                df = df.sort_values('order_date')

                k1, k2, k3 = st.columns(3)
                with k1:
                    st.metric('Total Revenue', f'${df["total_revenue"].sum():,.2f}')
                with k2:
                    st.metric('Total Orders', f'{int(df["total_orders"].sum()):,}')
                with k3:
                    st.metric('Total Units Sold', f'{int(df["total_units_sold"].sum()):,}')

                st.markdown('#### Daily Revenue')
                chart_df = df.set_index('order_date')[['total_revenue']]
                st.line_chart(chart_df)

                with st.expander('View Raw Data'):
                    st.dataframe(df, use_container_width=True)
            else:
                st.info('No sales data found for the selected date range.')
        else:
            st.error(f'API error {response.status_code}: {response.text}')
    except Exception as e:
        st.error(f'Could not connect to the API: {e}')

st.markdown('---')

# SECTION 2 — Category Performance (Priya-2)
st.subheader('Revenue by Product Category')

if st.button('Load Category Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/category_performance')
        if response.status_code == 200:
            cat_data = response.json()
            if cat_data:
                df_cat = pd.DataFrame(cat_data)

                top_cat = df_cat.loc[df_cat['total_revenue'].idxmax(), 'category_name']
                c1, c2 = st.columns(2)
                with c1:
                    st.metric('Top Category by Revenue', top_cat)
                with c2:
                    st.metric('Total Categories', len(df_cat))

                st.markdown('#### Revenue by Category')
                st.bar_chart(df_cat.set_index('category_name')[['total_revenue']])

                st.markdown('#### Units Sold by Category')
                st.bar_chart(df_cat.set_index('category_name')[['total_units_sold']])

                display_df = df_cat[['category_name','total_orders','total_units_sold','total_revenue','avg_selling_price']].copy()
                display_df['total_revenue'] = display_df['total_revenue'].map('${:,.2f}'.format)
                display_df['avg_selling_price'] = display_df['avg_selling_price'].map('${:,.2f}'.format)
                display_df.columns = ['Category','Orders','Units Sold','Total Revenue','Avg Selling Price']
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info('No category data available.')
        else:
            st.error(f'API error {response.status_code}: {response.text}')
    except Exception as e:
        st.error(f'Could not connect to the API: {e}')
