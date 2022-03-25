#App A: busca subir el archivo a S3 y asociarlo a un nombre de paciente en Examenes.csv
#prueba1: editar csv
#prueba2: subir .wav


#posibles mejoras:
 #arreglar que con tildes no se buguee
 #arreglar que no suba nada al csv si no se subio archivo .wav
 #arreglar que por deecto tire los examenes a una carpeta y con un nombre dependiendo del dia y hora para que no sobreescriba

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


#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlit3.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app2/appA/appAv4.py ubuntu@ec2-3-92-65-169.compute-1.amazonaws.com:/home/ubuntu/appAv4.py


bucketname='avm-test-bucket0'
s3 = boto3.resource('s3')


'''
# Subir Examen
'''
input_nombre = st.text_input("Ingrese nombre del Paciente" ,"Nombre Apellido" )
input_RUT = st.text_input("Ingrese RUT del Paciente" ,"12.345.678-9" )
input_Edad = st.text_input("Ingrese Edad del Paciente" ,"99" )
input_Patologico = st.text_input("Muestra patológica Si/No" ,"No" )
input_examen = st.text_input("Ingrese nombre del archivo" ,"nombre_carpeta/nombre_archivo.wav" )
#input_examen = 'testapp2/examenes/'+input_examen

#texto=input_nombre+","+input_examen+"\n"
texto=input_nombre+","+input_examen+","+input_RUT+","+input_Edad
texto=texto+",22-02-28,15:15,"+input_Patologico+",AVM99,50,50\n"

uploaded_file = st.file_uploader("Escoger archivo")
if uploaded_file is not None:
          # To read file as bytes:
          bytes_data = uploaded_file.getvalue()

if st.button('Subir Examen'):
    #actualizar csv
    object = s3.Object(bucketname, 'examenes.csv')
    body = object.get()['Body'].read()
    data=body+str.encode(texto)
    result = object.put(Body=data)
    
    #subir .wav a s3
    object2 = s3.Object(bucketname, input_examen)
    result = object2.put(Body=bytes_data)
    st.write("examen subido")




















