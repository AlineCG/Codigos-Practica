Esta app busca leer y poblar la base de datos desde ec2


tutorial1: https://www.youtube.com/watch?v=XDMgXZUfa10

(Crear servidor y base de datos inicial desde RDS)

id : DB-instance-AVM
usuario: postgres0
contraseña: ClaveAVM

vpc security group : test-AVM-security-group
zona de disponibilidad: Sin preferencia

base de datos inicial: AVM1BD


CONEXION:
Nombre de usuario maestro
postgres0
Contraseña maestra
ClaveAVM
Punto de enlace
db-instance-avm.chhggqnb5jji.us-east-1.rds.amazonaws.com


tutorial 2: https://www.youtube.com/watch?v=3jyPcAr49bM
(Conectar a PG admin y crear tablas)

Se crean las tablas
y al ultimo la que tendra foreign keys (se agregan en la seccion de constraints)

tutorial 3: https://www.youtube.com/watch?v=1z1ZFVLUhv0
(conectarse desde el cmd a la BD mediante psql)
psql -h db-instance-avm.chhggqnb5jji.us-east-1.rds.amazonaws.com -U postgres0 -d AVM1BD -p 5432
se ingresa la clave
>> \dt+
>> Select * from examenes 

tutorial4:
https://www.postgresqltutorial.com/postgresql-python/connect/

installar psycopg2 :
https://stackoverflow.com/questions/11583714/install-psycopg2-on-ubuntu

conectar la instancia EC2
https://www.youtube.com/watch?v=ypWzL3PdKx0
(agregar el mismo grupo de seguridad a ambas instancias y en la instancia de RDS agregar la conexion TCP con id privada de ec2

hacer querys con psycopg2:
https://www.postgresqltutorial.com/
(asegurar que se suba la actualizacion de la tabla)
https://www.lewuathe.com/python/postgresql/remind-for-insert-into-with-psycopg2.html


correr en pg admin: (nombres en minuscula para no tener problemas en las QUERYS)

CREATE TABLE pacientes(
rut VARCHAR(12) PRIMARY KEY,
nombre VARCHAR(30) NOT NULL,
edad int NOT NULL

);


CREATE TABLE profesionales(
rut VARCHAR(12) PRIMARY KEY,
nombre VARCHAR(30) NOT NULL
);


CREATE TABLE examenes(
id_examen INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY ,
archivo_audio VARCHAR(20) NOT NULL,
paciente_id VARCHAR(13) NOT NULL,
profesional_id VARCHAR(13) NOT NULL,
patologico VARCHAR(2) NOT NULL,

FOREIGN KEY (paciente_id) REFERENCES pacientes("rut") ON DELETE CASCADE,
FOREIGN KEY (profesional_id) REFERENCES profesionales("rut") ON DELETE CASCADE

);


