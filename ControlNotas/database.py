import mysql.connector
import pandas as pd
import os
#conexion bd
def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )

def obtenerusuarios(UserName):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    
    # Nota la coma después de UserName para que sea una tupla
    cursor.execute("SELECT * FROM usuarios WHERE UserName=%s", (UserName,))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario

def obtenerestudiantes():
    conn = conectar()
    query = "SELECT * FROM estudiantes"
    
    # Cambiamos read_excel por read_sql
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df

#Registrar estudiante 
def insertar_estudiante(NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno):
    conn = conectar()
    cursor = conn.cursor()

    query ="""INSERT INTO estudiantes (NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno) 
    values (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, (NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno))
    conn.commit()
    conn.close()
    



if __name__ == "__main__":
    try:
        conn = conectar()
        print("Conexión Exitosa")
        
        
        conn.close()
    except Exception as e:
        print(f"Error al conectar: {e}")