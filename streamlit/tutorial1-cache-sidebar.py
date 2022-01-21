import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
df = st.cache(pd.read_csv)("addresses.csv")
cities = st.sidebar.multiselect('Show Person for city?', df['ciudad'].unique())
estates = st.sidebar.multiselect('Show Person from estate?', df['estado'].unique())
new_df = df[(df['ciudad'].isin(cities)) & (df['estado'].isin(estates))]
st.write(new_df)
# Create distplot with custom bin_size
fig = px.scatter(new_df, x ='nombre',y='codigo postal',color='estado')
# Plot!
st.plotly_chart(fig)
