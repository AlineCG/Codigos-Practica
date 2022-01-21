import streamlit as st
x = st.slider('x')
st.write(x, 'squared is', x * x)

#se ejecuta con streamlit run helloworld.py desde cmd en la carpeta donde se encuentre el .py
