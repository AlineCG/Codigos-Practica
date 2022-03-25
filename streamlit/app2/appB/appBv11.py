#Esta plataforma permite visualizar un examen y procesarlo.

#v9 pero con arreglos (downsampling)

#posible mejora: si actualizo la pagina el formulario mantiene los ultimos valores pero el procesamiento se realiza con el valor por defecto (no el mostrado) -> hay que actualizar

#https://mail.python.org/pipermail/scipy-dev/2016-September/021531.html

import matplotlib
import streamlit as st
import pandas as pd 
import numpy as np


#conexión s3
import boto3
from io import BytesIO

#análisis
import io
from scipy.io import wavfile
import scipy.io as sio
import SIBIF_output_Journal_Z_Scores as SIBIF
import spl

#FFT
from scipy.fft import fft, fftfreq

#graficar
import scipy.io.wavfile as sciwav
import matplotlib.pyplot as plt
import resampy

#graficar desde backend
from matplotlib.backends.backend_agg import RendererAgg
import matplotlib
matplotlib.use("agg")
_lock = RendererAgg.lock


#pscp -i C:\Users\aline\Desktop\Practica-LANEK\codigos-streamlit\app2\instancias\streamlitv4.ppk C:/Users/aline/Desktop/Practica-LANEK/codigos-streamlit/app2/appBv3/appB/appBv11.py ubuntu@ec2-54-172-174-220.compute-1.amazonaws.com:/home/ubuntu/appBv11.py



###conexión  S3
bucketname='avm-test-bucket0'
s3 = boto3.resource('s3')
client = boto3.client('s3')

@st.cache
def leer_registro():
    return pd.read_csv("s3://avm-test-bucket0/examenes.csv")
    
df_examenes=leer_registro()   

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

@st.cache
def leer_audio(option): 
    obj = s3.Object(bucketname, option)
    body = obj.get()['Body'].read()
    return BytesIO(body)

wrapper=leer_audio(option)    
#wav_file = sciwav.read(wrapper)


###FICHA Paciente
df2=df_examenes[df_examenes['archivo_audio'].str.contains(option)]  #si se reescribe un archivo de audio con el mismo nombre mediante la plataforma A, quedara escrito dos veces en el .csv y fallará el código de la ficha


def ficha():
    st.write(' Paciente:',df2.nombre_apellido.item())    
    st.write(' RUT: ',df2.RUT.item())
    st.write(' Edad:',str(df2.Edad.item()))
    st.write(' Patológico: ',df2.Patológico.item())
    st.write(' Fecha/Hora de Examen:',df2.Fecha.item(),' ',df2.Hora.item())
    st.write(' Dispositivo: ',df2.Dispositivo.item())



#### ANÁLISIS
font = {"size": 22}
plt.rc("font", **font)

samplerate, data = wavfile.read(wrapper)

#revisar si tiene 1 o dos canales
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

#separar canales
canal1=[]
for i in range( len(data)-1):
    canal1.append(data[i][0])
canal2=[]
for i in range( len(data)-1):
    canal2.append(data[i][1])

canal1=np.array(canal1)
canal2=np.array(canal2)

#Resample for plotting
new_rate=samplerate/10
values_resampled=[int(values[0]/10),int(values[1]/10)]

canal1_resampled = resampy.resample(canal1, samplerate, new_rate)
canal2_resampled = resampy.resample(canal2, samplerate, new_rate)


dt_res = 1 / new_rate
ta_res = a * dt_res
import math
tb_res = (int(math.floor(b/10))) * dt_res

tab_res = resampy.resample(tab, samplerate, new_rate)


#### Selección de parámetros mediante formulario (permite que la página no actualice por cada parametro que se quiera cambiar)
#default
Q1 = 1.0
Q2 = 1.0
Q3 = 1.0
gain = 1.0

show_ficha = True #ficha paciente
show_graf1 = True #gráfica temporal
show_graf2 = True #gráfica gvv
show_graf3 = True #gráfica FFT


#Formulario
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
            values_resampled=[int(values[0]/10),int(values[1]/10)]
            show_ficha=ficha_form
            show_graf1=g1_form
            show_graf2=g2_form
            show_graf3=g3_form



### Gráficas
def hash_spines(spines:matplotlib.spines.Spines):
    return [s.color for s in spines]


@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_señal(values,option):                      #argumentos más rápidos de revisar por caching 
#def graf_señal (values,canal1,canal2,tab_res):     #verdaderos argumentos de la función  (para no trabajar con variables globales) 

    #resampling: tab_res, canal1_resampled, canal2_resampled
    fig, ax = plt.subplots()
    ax.plot(tab_res[values[0] : values[1]], canal1_resampled[values[0] : values[1]])
    ax.set(
        xlabel="Tiempo [s]",
        ylabel="Amplitud",
    )
    ax.grid()
    ax.legend(["Microphone", "Accelerometer"])
    fig.set_size_inches(20, 8)
       
    fig2, ax2 = plt.subplots()
    ax2.plot(tab_res[values[0] : values[1]], canal2_resampled[values[0] : values[1]])
    ax2.set(
        xlabel="Tiempo [s]",
        ylabel="Amplitud",
    )
    ax2.grid()
    ax2.legend(["Accelerometer"])
    fig2.set_size_inches(20, 8)

    return fig,fig2


def get_gvv(data,Q1,Q2,Q3,gain):    
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


@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_gvv(gvv,values):   #argumentos para caching
#def graf_gvv(tab,gvv):     #verdaderos argumentos (s/variables globales)
    fig2, ax2 = plt.subplots()
    ax2.plot(tab[values[0] : values[1]], gvv[values[0] : values[1]])
    ax2.set(
        xlabel="Tiempo [s]",
        ylabel="Amplitud",
    )
    ax2.grid()
    fig2.set_size_inches(20, 8)    
    return fig2

@st.cache(hash_funcs={matplotlib.figure.Figure:hash})
def graf_fft(option): #argumentos para caching
#def graf_fft(tb_res,canal1_resampled)

    #sin resampling
    #N   = int(samplerate * tb)
    #yf = fft(parte)
    #xf = fftfreq(N, 1 /samplerate)

    #con resampling
    N1  = int(new_rate * tb_res)
    yf = fft(canal1_resampled)
    xf = fftfreq(N1, 1/new_rate)

    fig3, ax3 = plt.subplots()
     
     
    if(len(yf)<len(xf)): 
        ax3.plot(xf[0:-1], np.abs(yf))
    else:
        ax3.plot(xf, np.abs(yf))

    ax3.set(
            xlabel="Frecuencia [Hz]",
            ylabel="Amplitud",
        )
    ax3.grid()
    fig3.set_size_inches(20, 8)
    return fig3


fig1,fig11=graf_señal(values_resampled,option)  #usar values (S/resampling)

gvv=get_gvv(data,Q1,Q2,Q3,gain)

fig2=graf_gvv(gvv,values)

fig3=graf_fft(option)


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
            st.markdown("Gráfico Temporal")
            st.pyplot(fig1)
            st.pyplot(fig11)

        if show_graf3:
            st.markdown("Gráfico FFT")
            st.pyplot(fig3)

        if show_graf2:
            st.markdown("Gráfico GVV")
            st.pyplot(fig2)
    else:
        st.markdown("Seleccione archivo válido para procesar (audio con 2 canales: acelerómetro y micrófono)")
    


