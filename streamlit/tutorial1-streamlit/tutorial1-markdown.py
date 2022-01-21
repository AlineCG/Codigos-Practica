import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
'''
# Club and Nationality AppThis very simple webapp allows you to select and visualize players from certain clubs and certain nationalities.
'''
df = st.cache(pd.read_csv)("addresses.csv")
cities = st.sidebar.multiselect('Show Player from city?', df['ciudad'].unique())
estates = st.sidebar.multiselect('Show Player from estate?', df['estado'].unique())
new_df = df[(df['ciudad'].isin(cities)) & (df['estado'].isin(estates))]
st.write(new_df)
# Create distplot with custom bin_size
fig = px.scatter(new_df, x ='nombre',y='codigo postal',color='estado')
'''
### Here is a simple chart between player codigo postal and estado
'''
st.plotly_chart(fig)
