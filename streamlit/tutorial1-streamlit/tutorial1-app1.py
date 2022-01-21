import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv("addresses.csv")
cities = st.multiselect('Show Person from city?', df['ciudad'].unique())
estados = st.multiselect('Show Person from estate?', df['estado'].unique())
# Filter dataframe
new_df = df[(df['ciudad'].isin(cities)) & (df['estado'].isin(estados))]
# write dataframe to screen
st.write(new_df)
