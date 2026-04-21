# 32_Product_Performance.py
# Sell-through rate and inventory turnover analysis
# Serves Priya Nair — Business Analyst (Persona 3)
# User Stories: Priya-3, Priya-4
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
    page_title = 'Product Performance — Stockly',
    page_icon  = '🏷️',
    layout     = 'wide'
)

API_BASE = 'http://api:4000/api'

# ------------------------------------------------
# Page header
# ------------------------------------------------
st.title('🏷️ Product Performance')
st.markdown(
    'Analyse sell-through rates and inventory turnover '
    'ratios to identify your best and worst performers.'
)
st.markdown('---')

# ------------------------------------------------
# SECTION 1 — Sell-Through Rate (Priya-3)
# Calls GET /analytics/sell_through?days=N
# ------------------------------------------------
st.subheader('Sell-Through Rate by SKU')
st.markdown(
    'Sell-through rate = units sold ÷ (units sold + current stock), '
    'expressed as a percentage. Higher is better.'
)

days_option = st.radio(
    'Time Window',
    options   = [30, 60, 90],
    index     = 2,         # default to 90 days
    horizontal= True,
    format_func = lambda x: f'Last {x} days'
)

if st.button('Load Sell-Through Data', type='primary'):
    try:
        response = requests.get(
            f'{API_BASE}/analytics/sell_through',
            params={'days': days_option}
        )

        if response.status_code == 200:
            st_data = response.json()

            if st_data:
                df_st = pd.DataFrame(st_data)

                # KPI cards
                s1, s2, s3 = st.columns(3)
                with s1:
                    avg_rate = df_st['sell_through_rate_pct'].mean()
                    st.metric('Avg Sell-Through Rate', f'{avg_rate:.1f}%')
                with s2:
                    top_sku = df_st.iloc[0]
                    st.metric(
                        'Top Performer',
                        top_sku['sku'],
                        f'{top_sku["sell_through_rate_pct"]:.1f}%'
                    )
                with s3:
                    bottom_sku = df_st.iloc[-1]
                    st.metric(
                        'Lowest Performer',
                        bottom_sku['sku'],
                        f'{bottom_sku["sell_through_rate_pct"]:.1f}%'
                    )

                # Bar chart — top 15 SKUs by sell-through rate
                st.markdown('#### Top 15 SKUs by Sell-Through Rate')
                chart_df = df_st.head(15).set_index('sku')[
                    ['sell_through_rate_pct']
                ]
                st.bar_chart(chart_df)

                # Full table
                st.markdown('#### Full Sell-Through Table')
                display_df = df_st[[
                    'sku', 'product_name', 'category_name',
                    'units_sold', 'current_stock', 'sell_through_rate_pct'
                ]].copy()
                display_df['sell_through_rate_pct'] = display_df[
                    'sell_through_rate_pct'
                ].map('{:.1f}%'.format)
                display_df.columns = [
                    'SKU', 'Product', 'Category',
                    'Units Sold', 'Current Stock', 'Sell-Through Rate'
                ]
                st.dataframe(display_df, use_container_width=True)

            else:
                st.info('No sell-through data available.')

        else:
            st.error(f'API error {response.status_code}: {response.text}')

    except Exception as e:
        st.error(f'Could not connect to the API: {e}')

st.markdown('---')

# ------------------------------------------------
# SECTION 2 — Inventory Turnover (Priya-4)
# Calls GET /analytics/turnover
# ------------------------------------------------
st.subheader('Inventory Turnover Ratio by SKU')
st.markdown(
    'Turnover ratio = total units sold ÷ current stock. '
    'A higher ratio means stock is moving faster relative to what is on hand.'
)

if st.button('Load Turnover Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/turnover')

        if response.status_code == 200:
            to_data = response.json()

            if to_data:
                df_to = pd.DataFrame(to_data)

                # KPI cards
                t1, t2 = st.columns(2)
                with t1:
                    avg_ratio = df_to['turnover_ratio'].mean()
                    st.metric('Avg Turnover Ratio', f'{avg_ratio:.2f}')
                with t2:
                    zero_turn = (df_to['turnover_ratio'] == 0).sum()
                    st.metric(
                        'Products with Zero Turnover',
                        int(zero_turn),
                        help='Products with stock but no recorded sales'
                    )

                # Bar chart — top 15 by turnover
                st.markdown('#### Top 15 SKUs by Turnover Ratio')
                chart_df = df_to.head(15).set_index('sku')[['turnover_ratio']]
                st.bar_chart(chart_df)

                # Full table
                st.markdown('#### Full Turnover Table')
                display_df = df_to[[
                    'sku', 'product_name', 'category_name',
                    'total_units_sold', 'quantity_on_hand', 'turnover_ratio'
                ]].copy()
                display_df['turnover_ratio'] = display_df[
                    'turnover_ratio'
                ].map('{:.2f}'.format)
                display_df.columns = [
                    'SKU', 'Product', 'Category',
                    'Total Units Sold', 'Current Stock', 'Turnover Ratio'
                ]
                st.dataframe(display_df, use_container_width=True)

            else:
                st.info('No turnover data available.')

        else:
            st.error(f'API error {response.status_code}: {response.text}')

    except Exception as e:
        st.error(f'Could not connect to the API: {e}')
