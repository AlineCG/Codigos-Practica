import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px

import boto3
client = boto3.client('s3')
path='s3://testbucket-lanek-0/carpeta0/footbal_data1.csv'

'''
# Club and Nationality App
This very simple webapp allows you to select and visualize players from certain clubs and certain nationalities.
'''
df = st.cache(pd.read_csv)(path)

clubs = st.sidebar.multiselect('Show Player for clubs?', df['Club'].unique())
nationalities = st.sidebar.multiselect('Show Player from Nationalities?', df['Nationality'].unique())

new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]
st.write(new_df)

# Create distplot with custom bin_size
fig = px.scatter(new_df, x ='Overall',y='Age',color='Name')

'''
### Here is a simple chart between player age and overall
'''

st.plotly_chart(fig)
