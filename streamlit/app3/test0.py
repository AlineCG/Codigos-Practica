
#conexion BD
import streamlit as st
import psycopg2
conn = psycopg2.connect(
    host="db-instance-avm.chhggqnb5jji.us-east-1.rds.amazonaws.com",
    database="AVM1BD",
    user="postgres0",
    password="ClaveAVM")


cur = conn.cursor()

## Filtro por paciente
cur.execute("""
        SELECT *
        FROM pacientes
        """)
rows = cur.fetchall()

lista_pacientes=[]
for row in rows:
    string1=row[1]+","+row[0]
    lista_pacientes.append(string1)
#st.write(rows)

#filtro por nombre de paciente
nombre_escogido = st.sidebar.selectbox('Pacientes', lista_pacientes)

#print(nombre_escogido)

nombre_paciente1 = nombre_escogido.split(",")
rut_paciente1=nombre_paciente1[1]
#print(rut_paciente1)

#examenes filtrado por nombre


####
query1 = "select * from examenes where paciente_id = %s"
query1 = "select rut from pacientes"
cur.execute (query1,(rut_paciente1,))

rows = cur.fetchall()
#st.write(rows)



lista_examenes=[]
for row in rows:
    #string1=row[1]+","+row[0]
    #lista_pacientes.append(string1)
    print(row)



query2 = "select * from pacientes where rut = %s"
cur.execute (query2,(rut_paciente1,))
rows = cur.fetchall()
info_paciente=[]
for row in rows:
    info_paciente.append(row)

#print(rows)
#st.write(rows)


query3 = "select * from examenes inner join profesionales on examenes.profesional_id=profesionales.rut where (examenes.paciente_id = %s AND examenes.archivo_audio = %s) "

#query3 = "select * from examenes inner join profesionales on examenes.profesional_id=profesionales.rut where examenes.archivo_audio = %s "



a='22.222.222-2'
b='test25.wav'
cur.execute (query3,(a,b,))
#cur.execute(query3,(b,))

rows = cur.fetchall()
info_examen=[]
for row in rows:
    info_examen.append(row)

print("info examen")
print (info_examen)




