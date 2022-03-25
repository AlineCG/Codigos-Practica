#esta version busca leer los arhivos del bucket para elegir alguno y abrir el .wav (arreglar boton upload)

#https://mail.python.org/pipermail/scipy-dev/2016-September/021531.html

import streamlit as st
#import pandas as pd #este no se si se usa
import numpy as np

#graficar
#import wave
import matplotlib.pyplot as plt

#
import boto3
#import io
from io import BytesIO
import scipy.io.wavfile as sciwav

#pscp -i C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/tutorial2-ec2/streamlit.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app1/app1.4.py ubuntu@ec2-34-229-167-180.compute-1.amazonaws.com:/home/ubuntu/app1.4.py
#pscp -i C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/tutorial2-ec2/streamlit.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app1/test0.wav ubuntu@ec2-34-229-167-180.compute-1.amazonaws.com:/home/ubuntu/test0.wav

bucketname='testbucket-lanek-0'
itemname='testapp1/test0.wav'
s3 = boto3.resource('s3')

###
lista_de_objetos=[]
bucket=s3.Bucket(bucketname)
for obj in bucket.objects.all():
    print(obj.key)
    lista_de_objetos.append(obj.key)

###
option=st.selectbox("Escoja archivo a procesar", lista_de_objetos)

### escoger uno y mostrar grafica
#obj = s3.Object(bucketname, itemname)
obj = s3.Object(bucketname, option)
body = obj.get()['Body'].read()

wrapper = BytesIO(body)

wav_file = sciwav.read(wrapper)


'''
# Audio Wave 
'''


#print("JAJAA")
#print(wav_file)
#print("HOLA")
#print(wav_file[1])


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
# UPLOADDDD
'''
#todavia no funciona con esto del boton
if st.button('Subir archivo'):
    uploaded_file = st.file_uploader("Escoger archivo")
    if uploaded_file is not None:
          # To read file as bytes:
          bytes_data = uploaded_file.getvalue()
          #st.write(bytes_data)
          user_input = st.text_input("Ingrese nombre del archivo en bucket (nombrecarpeta/nombrearchivo.ext)" )
          print("HOLA")
          print(user_input)
          #object = s3.Object('testbucket-lanek-0', 'carpeta0/test0.wav')
          object = s3.Object('testbucket-lanek-0', user_input)
          result = object.put(Body=bytes_data)

#tira error pues intenta guardarlo antes de que el usuario ingrese el nombre del archivo en s3












