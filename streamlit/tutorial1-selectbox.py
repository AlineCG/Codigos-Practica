import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv("addresses.csv")

option = st.selectbox(
    'Which City do you like best?', df['ciudad'].unique())

'You selected: ', option
