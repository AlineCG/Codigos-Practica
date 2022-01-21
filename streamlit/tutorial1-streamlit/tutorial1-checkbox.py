
import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv("addresses.csv", encoding='latin-1')
if st.checkbox('Show dataframe'):
#   st.write("hola!")
    st.write(df)
#se ejecuta con streamlit run helloworld.py desde cmd en la carpeta donde se encuentre el .py
