import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
df = pd.read_csv("addresses.csv")
cities = st.multiselect('Show Person for city?', df['ciudad'].unique())
estates = st.multiselect('Show Person from estate?', df['estado'].unique())
new_df = df[(df['ciudad'].isin(cities)) & (df['estado'].isin(estates))]
st.write(new_df)
# create figure using plotly express
fig = px.scatter(new_df, x ='nombre',y='codigo postal',color='apellido')
# Plot!
st.plotly_chart(fig)

#plotly express no viene con streamlit
