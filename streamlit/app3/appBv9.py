#leer los arhivos del bucket para elegir alguno y abrir el .wav

#v9 (Sin downsampling)

#se agrega implementación de BD

#mejoras pendientes:
# - si no tiene ningun examen el paciente recien agregado
# - Agregar datos de AVM, ganancias y fecha desde el nombre del archivo

#https://mail.python.org/pipermail/scipy-dev/2016-September/021531.html

import matplotlib
import streamlit as st
import pandas as pd 
import numpy as np

#graficar
import scipy.io.wavfile as sciwav
import matplotlib.pyplot as plt

#
import boto3
from io import BytesIO

#pip install fsspec
#pip install s3fs

#analisis
import io
from scipy.io import wavfile
import scipy.io as sio
import SIBIF_output_Journal_Z_Scores as SIBIF
import spl


#FFT
from scipy.fft import fft, fftfreq

#
from matplotlib.backends.backend_agg import RendererAgg

import matplotlib
matplotlib.use("agg")
_lock = RendererAgg.lock


#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlitv2.ppk C:\Users\aline\Desktop\BD-AVM\app3\appB\appBv9.py ubuntu@ec2-44-202-82-222.compute-1.amazonaws.com:/home/ubuntu/appBv9.py

#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlitv2.ppk C:\Users\aline\Desktop\BD-AVM\app3\appB\appBv9.py ubuntu@ec2-50-16-106-236.compute-1.amazonaws.com:/home/ubuntu/appBv9.py



###conexión  S3
bucketname='avm-test-bucket0'
s3 = boto3.resource('s3')

client = boto3.client('s3')

#conexion BD

import psycopg2
conn = psycopg2.connect(
    host="db-instance-avm.chhggqnb5jji.us-east-1.rds.amazonaws.com",
    database="AVM1BD",
    user="postgres0",
    password="ClaveAVM")


cur = conn.cursor()

## Filtro por paciente
cur.execute("""
        SELECT pacientes.rut, pacientes.nombre
        FROM pacientes
        """)
rows = cur.fetchall()

lista_pacientes=[]
for row in rows:
    string1=row[1]+","+row[0]
    lista_pacientes.append(string1)

#filtro por nombre de paciente
nombre_escogido = st.sidebar.selectbox('pacientes', lista_pacientes)

nombre_paciente1 = nombre_escogido.split(",")
rut_paciente1=nombre_paciente1[1]

#examenes filtrado por nombre
query1 = "select examenes.archivo_audio from examenes where paciente_id = %s"
cur.execute (query1,(rut_paciente1,))
rows = cur.fetchall()


info_examenes=[]
for row in rows:
    string1=row[0]
    info_examenes.append(string1)

st.sidebar.write('''# SELECCIONAR EXAMEN ''')
option=st.sidebar.selectbox("Escoja archivo a procesar", info_examenes)



@st.cache
def leer_audio(option): 
    obj = s3.Object(bucketname, option)
    body = obj.get()['Body'].read()
    return BytesIO(body)

wrapper=leer_audio(option)    
#wav_file = sciwav.read(wrapper)


###FICHA Paciente
#ojo si se reescribe un archivo de audio con el mismo nombre mediante la plataforma A, quedara escrito dos veces en el .csv y fallará el código de la ficha
query2 = "select * from pacientes where rut = %s"
query3 = "select examenes.patologico, profesionales.nombre from examenes inner join profesionales on examenes.profesional_id=profesionales.rut where (examenes.paciente_id = %s AND examenes.archivo_audio = %s) "

cur.execute (query2,(rut_paciente1,))
rows = cur.fetchall()
info_paciente=[]
for row in rows:
    info_paciente.append(row)

cur.execute (query3,(rut_paciente1,option,))
#cur.execute (query3,(rut_paciente1,))

rows = cur.fetchall()
info_examen=[]
for row in rows:
    info_examen.append(row)

print("info examen")
print (info_examen)

def ficha():
    st.write(' Paciente:',info_paciente[0][1])    
    st.write(' RUT: ',info_paciente[0][0])
    st.write(' Edad:',str(info_paciente[0][2]))
    st.write(' Patológico: ',info_examen[0][0])
    st.write(' Profesional:',info_examen[0][1])
#    st.write(' Fecha/Hora de Examen:',df2.Fecha.item(),' ',df2.Hora.item())
#    st.write(' Dispositivo: ',df2.Dispositivo.item())




#### ANALISIS
font = {"size": 22}
plt.rc("font", **font)

samplerate, data = wavfile.read(wrapper)


shape1=np.shape(data)
shapeofshape=np.shape(shape1)

a = 0
b = len(data)
dt = 1 / samplerate
ta = a * dt
tb = (b - 1) * dt
tab = np.arange(ta, tb, dt)
parte = data[a : b - 1]
values = [a, b]


#### Selección de parámetros mediante formulario (permite que la página no actualice por cada parametro que se quiera cambiar)
#default
Q1 = 1.0
Q2 = 1.0
Q3 = 1.0
gain = 1.0

show_ficha = True
show_graf1 = True #temporal
show_graf2 = True #gvv
show_graf3 = True #FFT


#formulario
with st.sidebar:
    with st.form("Set parameters"):
        
        values_form = st.slider("Select a range of values", a, b, (a, b))
        st.write("Set parameters")
        Q1_form = float(st.text_input("Q1", value='1.0'))
        Q2_form = float(st.text_input("Q2", value='1.0'))
        Q3_form = float(st.text_input("Q3", value='1.0'))
        gain_form = float(st.text_input("Gain", value='1.0'))
        ficha_form=st.checkbox('Mostrar Ficha Paciente',value=True)
        g1_form=st.checkbox('Mostrar Señal temporal',value=True)
        g3_form=st.checkbox('Mostrar FFT',value=True)
        g2_form=st.checkbox('Mostrar GVV',value=True)
        

    # Every form must have a submit button.
        submitted = st.form_submit_button("Procesar examen")
        if submitted:
            Q1=Q1_form
            Q2=Q2_form
            Q3=Q3_form
            gain=gain_form
            values=values_form
            show_ficha=ficha_form
            show_graf1=g1_form
            show_graf2=g2_form
            show_graf3=g3_form



### graficas
def hash_spines(spines:matplotlib.spines.Spines):
    return [s.color for s in spines]


#@st.cache(suppress_st_warning=True)
#@st.cache(hash_funcs={matplotlib.spines.Spines:hash_spines})
@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_señal(parte,tab):
    print("dentro func1")
    fig, ax = plt.subplots()
    ax.plot(tab[values[0] : values[1]], parte[values[0] : values[1]])
    ax.set(
        xlabel="Tiempo [s]",
        ylabel="Amplitud",
    )
    ax.grid()
    ax.legend(["Microphone", "Accelerometer"])
    fig.set_size_inches(20, 8)
    #st.pyplot(fig)        
    print("dentro func 2")
    return fig

#@st.cache
def get_gvv(a,b,option,Q1,Q2,Q3,gain):
    ######### abrir archivo .wav ############
    dataACC = data[:, 1]
    ######## Parametros Q ############
    mat_contents = sio.loadmat("Weibel_IF_IBIF_GUI.mat")
    indexPos = 8
    indexLen = 5
    Hsub1 = mat_contents["Hsub1_cell"][indexLen - 1, indexPos - 1][0]
    Zsub2 = mat_contents["Zsub2_cell"][indexLen - 1, indexPos - 1][0]
    fWeibel = mat_contents["fWeibel"][0]
    ########### IBIF ###########
    gvv_acc = SIBIF.SIBIF_output_Journal_Z_Scores(
        Q1, Q2, Q3, gain, dataACC / 32767, fWeibel, Hsub1, Zsub2
    )
    gvv_acc2 = gvv_acc[0:-1]
    return gvv_acc2

#@st.cache
@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_gvv(gvv_acc2):
    fig2, ax2 = plt.subplots()
    ax2.plot(tab[values[0] : values[1]], gvv_acc2[values[0] : values[1]])
    ax2.set(
        xlabel="Tiempo [s]",
        ylabel="Amplitud",
    )
    ax2.grid()
    fig2.set_size_inches(20, 8)
    #st.pyplot(fig2)
    
    return fig2

#@st.cache
@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_fft(a,b,option): 
    # Number of samples in normalized_tone
    print("tb")
    print(tb)
    N   = int(samplerate * tb)
    yf = fft(parte)
    xf = fftfreq(N, 1 /samplerate)

    fig3, ax3 = plt.subplots()

    ax3.plot(xf, np.abs(yf))
    ax3.set(
            xlabel="Frecuencia [Hz]",
            ylabel="Amplitud",
        )
    ax3.grid()
    fig3.set_size_inches(20, 8)
    #st.pyplot(fig3)
    return fig3

print ("hola1")

fig1=graf_señal(parte,tab)

print("hola2")
gvv_acc2=get_gvv(a,b,option,Q1,Q2,Q3,gain)
fig2=graf_gvv(gvv_acc2)
fig3=graf_fft(a,b,option)


### Displaying
col1, col2= st.columns(2)
            
with col1:            
    if show_ficha:
        '''
        # PACIENTE
        '''
        ficha()

    
with col2,_lock:
    '''
    # EXAMEN
    '''  
    if(shapeofshape[0]==2):
        if show_graf1:
            #graf_señal()
            print("holaA")
            st.markdown("Gráfico Temporal")
            st.pyplot(fig1)
            print("holaB")

        if show_graf3:
            #graf_fft()
            st.markdown("Gráfico FFT")
            st.pyplot(fig3)

        if show_graf2:
            #graf_gvv(gvv)
            st.markdown("Gráfico GVV")
            st.pyplot(fig2)
    else:
        st.markdown("Seleccione archivo válido para procesar (audio con 2 canales: acelerómetro y micrófono)")
    


