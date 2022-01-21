import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv("addresses.csv")
options = st.multiselect(
 'What are your favorite city?', df['ciudad'].unique())
st.write('You selected:', options)
