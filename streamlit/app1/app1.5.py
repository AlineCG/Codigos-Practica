#esta version busca leer los arhivos del bucket para elegir alguno y abrir el .wav (arreglar boton upload)
#objetivos:
#arreglar boton upload ->
#eliminar elementos que no sean .wav del select box  ->LISTO


#https://mail.python.org/pipermail/scipy-dev/2016-September/021531.html

import streamlit as st
#import pandas as pd #este no se usa
import numpy as np

#graficar
import scipy.io.wavfile as sciwav
import matplotlib.pyplot as plt

#
import boto3
from io import BytesIO

#pscp -i C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/tutorial2-ec2/streamlit.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app1/app1.5.py ubuntu@ec2-34-229-167-180.compute-1.amazonaws.com:/home/ubuntu/app1.5.py
#pscp -i C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/tutorial2-ec2/streamlit.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app1/test0.wav ubuntu@ec2-34-229-167-180.compute-1.amazonaws.com:/home/ubuntu/test0.wav

bucketname='testbucket-lanek-0'
itemname='testapp1/test0.wav'
s3 = boto3.resource('s3')


'''
# SELECT FILE
'''

###
lista_de_objetos=[]
bucket=s3.Bucket(bucketname)
for obj in bucket.objects.all():
    print(obj.key)
    if '.wav' in obj.key:
        lista_de_objetos.append(obj.key)

### escoger uno y mostrar grafica
option=st.selectbox("Escoja archivo a procesar", lista_de_objetos)
#obj = s3.Object(bucketname, itemname)
obj = s3.Object(bucketname, option)
body = obj.get()['Body'].read()
wrapper = BytesIO(body)
wav_file = sciwav.read(wrapper)


'''
# Audio Wave 
'''

#plt.rcParams["figure.figsize"] = [7.50, 3.50]
#plt.rcParams["figure.autolayout"] = True

audio = wav_file[1]

fig= plt.figure(1)
#plt.plot(audio[0:1240])
plt.plot(audio)
plt.ylabel("Amplitude")
plt.xlabel("Time")
#plt.show()
st.pyplot(fig)





'''
# UPLOAD
'''

#if st.button('Subir archivo'):
#    uploaded_file = st.file_uploader("Escoger archivo")
#    if uploaded_file is not None:
#          # To read file as bytes:
#          bytes_data = uploaded_file.getvalue()
#          #st.write(bytes_data)
#    user_input = st.text_input("Ingrese nombre del archivo en bucket (nombrecarpeta/nombrearchivo.ext)" )
#    print("HOLA")
#    print(user_input)
#          #object = s3.Object('testbucket-lanek-0', 'carpeta0/test0.wav')

#    object = s3.Object('testbucket-lanek-0', user_input)
#    result = object.put(Body=bytes_data)
#    st.write("archivo subido")
#tira error pues intenta guardarlo antes de que el usuario ingrese el nombre del archivo en s3




#with st.form("my_form"):
#    st.write("formulario subir archivo")
    
#    user_input = st.text_input("Ingrese nombre del archivo en bucket (nombrecarpeta/nombrearchivo.ext)" )

#    uploaded_file = st.file_uploader("Escoger archivo")
#    if uploaded_file is not None:
          # To read file as bytes:
#          bytes_data = uploaded_file.getvalue()
          
#    object = s3.Object('testbucket-lanek-0', user_input)
#    result = object.put(Body=bytes_data)
#    st.write("archivo subido")
    

    # Every form must have a submit button.
#    submitted = st.form_submit_button("Submit")
#    if submitted:
#        st.write("subidoooo")

#st.write("Outside the form")


#############

uploaded_file = st.file_uploader("Escoger archivo")
if uploaded_file is not None:
          # To read file as bytes:
          bytes_data = uploaded_file.getvalue()
          #st.write(bytes_data)
user_input = st.text_input("Ingrese nombre del archivo en bucket" ,"nombre_carpeta/nombre_archivo.wav" )

#object = s3.Object('testbucket-lanek-0', 'carpeta0/test0.wav')

if st.button('Subir archivo'):
    object = s3.Object('testbucket-lanek-0', user_input)
    result = object.put(Body=bytes_data)
    st.write("archivo subido")




