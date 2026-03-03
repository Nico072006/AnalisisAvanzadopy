import mysql.connector


def conectar ():
    conexion =mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="estudiantes"

    )
    return conexion 

if __name__=="__main__":
    coon=conectar()
    print("Conexion Exitosa")
    coon.close()