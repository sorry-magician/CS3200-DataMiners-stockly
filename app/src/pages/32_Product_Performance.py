import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(page_title='Product Performance — Stockly', page_icon='🏷️', layout='wide')
SideBarLinks()

if not st.session_state.get('authenticated'):
    st.warning('Please log in from the Home page first.')
    st.stop()

API_BASE = 'http://web-api:4000/api'

st.title('🏷️ Product Performance')
st.markdown('Analyse sell-through rates and inventory turnover ratios to identify your best and worst performers.')
st.markdown('---')

# SECTION 1 — Sell-Through Rate (Priya-3)
st.subheader('Sell-Through Rate by SKU')
st.markdown('Sell-through rate = units sold ÷ (units sold + current stock), expressed as a percentage.')

days_option = st.radio('Time Window', options=[30, 60, 90], index=2, horizontal=True, format_func=lambda x: f'Last {x} days')

if st.button('Load Sell-Through Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/sell_through', params={'days': days_option})
        if response.status_code == 200:
            st_data = response.json()
            if st_data:
                df_st = pd.DataFrame(st_data)

                s1, s2, s3 = st.columns(3)
                with s1:
                    st.metric('Avg Sell-Through Rate', f'{df_st["sell_through_rate_pct"].mean():.1f}%')
                with s2:
                    top = df_st.iloc[0]
                    st.metric('Top Performer', top['sku'], f'{top["sell_through_rate_pct"]:.1f}%')
                with s3:
                    bot = df_st.iloc[-1]
                    st.metric('Lowest Performer', bot['sku'], f'{bot["sell_through_rate_pct"]:.1f}%')

                st.markdown('#### Top 15 SKUs by Sell-Through Rate')
                st.bar_chart(df_st.head(15).set_index('sku')[['sell_through_rate_pct']])

                display_df = df_st[['sku','product_name','category_name','units_sold','current_stock','sell_through_rate_pct']].copy()
                display_df['sell_through_rate_pct'] = display_df['sell_through_rate_pct'].map('{:.1f}%'.format)
                display_df.columns = ['SKU','Product','Category','Units Sold','Current Stock','Sell-Through Rate']
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info('No sell-through data available.')
        else:
            st.error(f'API error {response.status_code}: {response.text}')
    except Exception as e:
        st.error(f'Could not connect to the API: {e}')

st.markdown('---')

# SECTION 2 — Inventory Turnover (Priya-4)
st.subheader('Inventory Turnover Ratio by SKU')
st.markdown('Turnover ratio = total units sold ÷ current stock. Higher means stock moves faster.')

if st.button('Load Turnover Data', type='primary'):
    try:
        response = requests.get(f'{API_BASE}/analytics/turnover')
        if response.status_code == 200:
            to_data = response.json()
            if to_data:
                df_to = pd.DataFrame(to_data)

                t1, t2 = st.columns(2)
                with t1:
                    st.metric('Avg Turnover Ratio', f'{df_to["turnover_ratio"].mean():.2f}')
                with t2:
                    st.metric('Products with Zero Turnover', int((df_to['turnover_ratio'] == 0).sum()))

                st.markdown('#### Top 15 SKUs by Turnover Ratio')
                st.bar_chart(df_to.head(15).set_index('sku')[['turnover_ratio']])

                display_df = df_to[['sku','product_name','category_name','total_units_sold','quantity_on_hand','turnover_ratio']].copy()
                display_df['turnover_ratio'] = display_df['turnover_ratio'].map('{:.2f}'.format)
                display_df.columns = ['SKU','Product','Category','Total Units Sold','Current Stock','Turnover Ratio']
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info('No turnover data available.')
        else:
            st.error(f'API error {response.status_code}: {response.text}')
    except Exception as e:
        st.error(f'Could not connect to the API: {e}')
