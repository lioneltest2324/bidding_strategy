import streamlit as st
import pandas as pd
import altair as alt
from universal_component_for_campaign import load_and_process_data,out_date_range_data,create_date_filtered_df,\
    output_groupby_df,add_custom_proportion_to_df,process_hk_cost_and_value_on_ads_data
st.set_page_config(layout="wide")
ads_url = 'https://docs.google.com/spreadsheets/d/1K__Mzx-lwk7USJXMj_MdvGmO2ud_3MIJpQAZ7IAkfzU/edit#gid=0'
raw_bidding_data = load_and_process_data(ads_url,1433014523)
raw_bidding_data['pmax_troas'] =raw_bidding_data['pmax_troas'].fillna(0)
raw_bidding_data['troas'] =raw_bidding_data['troas'].fillna(0)
raw_bidding_data.loc[(raw_bidding_data['status'].str.contains('PAUSED')),'strategy'] = '广告已关停'
raw_bidding_data.loc[(raw_bidding_data['status'].str.contains('ENABLED'))&(raw_bidding_data['bidding_strategy'].str.contains('MAXIMIZE_CONVERSION_VALUE')) & (raw_bidding_data['pmax_troas']==0), 'strategy'] = 'MAXIMIZE_VALUE'
raw_bidding_data.loc[(raw_bidding_data['status'].str.contains('ENABLED'))&(raw_bidding_data['bidding_strategy'].str.contains('MAXIMIZE_CONVERSION_VALUE')) & (raw_bidding_data['pmax_troas']!=0), 'strategy'] = \
    "Troas: " + (raw_bidding_data['pmax_troas'] * 100).astype(int).astype(str)+ "%"
raw_bidding_data.loc[(raw_bidding_data['status'].str.contains('ENABLED'))&(raw_bidding_data['bidding_strategy'].str.contains('TARGET_ROAS')) & (raw_bidding_data['troas']==0), 'strategy'] = 'MAXIMIZE_VALUE'
raw_bidding_data.loc[(raw_bidding_data['status'].str.contains('ENABLED'))&(raw_bidding_data['bidding_strategy'].str.contains('TARGET_ROAS')) & (raw_bidding_data['troas']!=0), 'strategy'] =\
    "Troas: " + (raw_bidding_data['troas'] * 100).astype(int).astype(str) + "%"
raw_bidding_data = raw_bidding_data.dropna(subset=['strategy'])
raw_bidding_data = raw_bidding_data.drop(columns=['troas','pmax_troas','status'])
st.dataframe(raw_bidding_data,width=2400,height=800)
