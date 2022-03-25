#App A: busca subir el archivo a S3 y asociarlo a un nombre de paciente en Examenes.csv



#obj: eliminar elementos.

#posibles mejoras:
 #auto refresh cuando se agrega un paciente/profesional nuevo
 #no sobreescribir archivo en S3
 #no sobreescribir paciente/profesional
 #arreglar que con tildes no se buguee
 #arreglar que no suba nada si no se ha subido un archivo 
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


#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlit3.ppk C:\Users\aline\Desktop\BD-AVM\app3\appAv6.py ubuntu@ec2-3-92-65-169.compute-1.amazonaws.com:/home/ubuntu/appAv6.py

#conexion S3
bucketname='avm-test-bucket0'
s3 = boto3.resource('s3')

#conexion BD

import psycopg2
conn = psycopg2.connect(
    host="db-instance-avm.chhggqnb5jji.us-east-1.rds.amazonaws.com",
    database="AVM1BD",
    user="postgres0",
    password="ClaveAVM")


cur = conn.cursor()



'''
# Subir Examen
'''
#leer BD

cur.execute("""
        SELECT *
        FROM profesionales
        """)
rows = cur.fetchall()

lista_profesionales=[]

for row in rows:
    string1=row[1]+","+row[0]
    lista_profesionales.append(string1)

cur.execute("""
        SELECT *
        FROM pacientes
        """)
rows = cur.fetchall()

lista_pacientes=[]

for row in rows:
    string1=row[1]+","+row[0]
    lista_pacientes.append(string1)




input_Paciente = st.selectbox('Paciente', lista_pacientes)
rut_paciente = input_Paciente.split(",")
rut_paciente=rut_paciente[1]

input_Profesional = st.selectbox('Profesional', lista_profesionales)
rut_profesional = input_Profesional.split(",")
rut_profesional=rut_profesional[1]

patolog=['no','si']
input_Patologico = st.selectbox("Muestra patológica" ,patolog)
input_examen = st.text_input("Ingrese nombre del archivo" ,"nombre_carpeta/nombre_archivo.wav" )


uploaded_file = st.file_uploader("Escoger archivo")
if uploaded_file is not None:
          # To read file as bytes:
          bytes_data = uploaded_file.getvalue()

if st.button('Subir Examen'):
    
    #actualizar BD

#    cur.execute("""
#        INSERT INTO Pacientes ("RUT", "Nombre", "Edad")
#        VALUES(%s,%s, %s);
#        """, (input_RUT,input_nombre,input_Edad))

    cur.execute(""" INSERT INTO examenes 
        ( "archivo_audio","paciente_id", "profesional_id", "patologico") 
        VALUES(%s,%s,%s,%s);""",
        (input_examen,rut_paciente,rut_profesional,input_Patologico) )

    conn.commit() 



    #subir .wav a s3
    object2 = s3.Object(bucketname, input_examen)
    result = object2.put(Body=bytes_data)
    st.write("examen subido")

st.sidebar.write('''# Ingresar nuevo paciente ''')

input_nombre = st.sidebar.text_input("Ingrese nombre del Paciente" ,"Nombre Apellido" )
input_RUT = st.sidebar.text_input("Ingrese RUT del Paciente" ,"12.345.678-9" )
input_Edad = st.sidebar.text_input("Ingrese Edad del Paciente" ,"99" )


if st.sidebar.button('Agregar Paciente'):
    cur.execute("""
       INSERT INTO pacientes ("rut", "nombre", "edad")
        VALUES(%s,%s, %s);
        """, (input_RUT,input_nombre,input_Edad))
    conn.commit() 
    st.sidebar.write("Paciente agregado")


st.sidebar.write('''# Ingresar nuevo profesional ''')

input_nombre_prof = st.sidebar.text_input("Ingrese nombre del Profesional" ,"Nombre Apellido" )
input_RUT_prof = st.sidebar.text_input("Ingrese RUT del Profesional" ,"12.345.678-9" )

if st.sidebar.button('Agregar Profesional'):
    cur.execute("""
       INSERT INTO profesionales ("rut", "nombre")
        VALUES(%s,%s);
        """, (input_RUT_prof,input_nombre_prof))
    conn.commit() 
    st.sidebar.write("Profesional agregado")
















