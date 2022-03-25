#leer los arhivos del bucket para elegir alguno y abrir el .wav

#v7 con arreglos
#obj: agregar backend agg rendering-> listo


#https://mail.python.org/pipermail/scipy-dev/2016-September/021531.html

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

from matplotlib.backends.backend_agg import RendererAgg

import matplotlib
matplotlib.use("agg")
_lock = RendererAgg.lock

#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlitv4.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app2/appBv3/appB/appBv10.py ubuntu@ec2-54-172-174-220.compute-1.amazonaws.com:/home/ubuntu/appBv10.py



###conexión  S3
bucketname='avm-test-bucket0'
s3 = boto3.resource('s3')

client = boto3.client('s3')
df_examenes = pd.read_csv("s3://avm-test-bucket0/examenes.csv")

#filtro por nombre de paciente
nombre_escogido = st.sidebar.multiselect('Pacientes', df_examenes['nombre_apellido'].unique())

#tabla de datos filtrada por nombre
new_df = df_examenes[df_examenes['nombre_apellido'].isin(nombre_escogido)]

#lista de archivos a abrir para el paciente seleccionado
st.sidebar.write('''# SELECCIONAR EXAMEN ''')
lista_de_objetos=[]
bucket=s3.Bucket(bucketname)
for obj in bucket.objects.all():   #si tira error en estas lineas puede ser porque hay archivos en el bucket que no esten en el .csv
    #print(obj.key)
    if (nombre_escogido):
        if ( ('.wav' in obj.key) &  (new_df['archivo_audio'].str.contains(obj.key).any()) ) :       
            lista_de_objetos.append(obj.key)
    else:  #('examen' in obj.key)
        if (('.wav' in obj.key) ):  
            lista_de_objetos.append(obj.key)

          
### Escoger uno y cargar a la página
option=st.sidebar.selectbox("Escoja archivo a procesar", lista_de_objetos)
obj = s3.Object(bucketname, option)
body = obj.get()['Body'].read()
wrapper = BytesIO(body)
#wav_file = sciwav.read(wrapper)


###FICHA Paciente

df2=df_examenes[df_examenes['archivo_audio'].str.contains(option)]
#st.table(df2)


def ficha():
    st.write(' Paciente:',df2.nombre_apellido.item())    
    st.write(' RUT: ',df2.RUT.item())
    st.write(' Edad:',str(df2.Edad.item()))
    st.write(' Patológico: ',df2.Patológico.item())
    st.write(' Fecha/Hora de Examen:',df2.Fecha.item(),' ',df2.Hora.item())
    st.write(' Dispositivo: ',df2.Dispositivo.item())




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

def graf_señal():
    # tiene 2 canales
    if(shapeofshape[0]==2):
        fig, ax = plt.subplots()
        ax.plot(tab[values[0] : values[1]], parte[values[0] : values[1]])
        st.markdown("Gráfico Temporal")
        ax.set(
            xlabel="Tiempo [s]",
            ylabel="Amplitud",
        )
        ax.grid()
        ax.legend(["Microphone", "Accelerometer"])
        fig.set_size_inches(20, 8)
        print("hola1")
        st.pyplot(fig,clear_figure=True)
        print("hola2")
    #archivo .wav tiene solo 1 canal
    if(shapeofshape[0]==1):
        st.markdown("Seleccione archivo válido para procesar (audio con 2 canales: acelerómetro y micrófono)")

def get_gvv():
    # tiene 2 canales
    if(shapeofshape[0]==2):
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
    
def graf_gvv(gvv_acc2):
    if(shapeofshape[0]==2):
        fig2, ax2 = plt.subplots()
        ax2.plot(tab[values[0] : values[1]], gvv_acc2[values[0] : values[1]])
        st.markdown("Gráfico GVV")
        ax2.set(
            xlabel="Tiempo [s]",
            ylabel="Amplitud",
        )
        ax2.grid()
        fig2.set_size_inches(20, 8)
        print("hola3")
        st.pyplot(fig2,clear_figure=True)
        print("hola4")

    #archivo .wav tiene solo 1 canal
    if(shapeofshape[0]==1):
        st.markdown("Seleccione archivo válido para procesar (audio con 2 canales: acelerómetro y micrófono)")

#FFT
from scipy.fft import fft, fftfreq
def graf_fft(): 
    # Number of samples in normalized_tone
    print("tb")
    print(tb)
    N   = int(samplerate * tb)
    yf = fft(parte)
    xf = fftfreq(N, 1 /samplerate)

    fig3, ax3 = plt.subplots()

    ax3.plot(xf, np.abs(yf))
    st.markdown("Gráfico FFT")
    ax3.set(
            xlabel="Frecuencia [Hz]",
            ylabel="Amplitud",
        )
    ax3.grid()
    fig3.set_size_inches(20, 8)
    st.pyplot(fig3,clear_figure=True)




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
    if show_graf1:
        graf_señal()

    if show_graf3:
        graf_fft()

    gvv=get_gvv()

    if show_graf2:
        graf_gvv(gvv)


