import pandas as pd
import unicodedata 
from flask import Flask, render_template, request, redirect, session
from database import conectar, obtenerusuarios, insertar_estudiante
from dashprincipal import creartablero

app = Flask(__name__)
app.secret_key = "1070464999"

# Configuración del tablero Dash
creartablero(app)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- FUNCIONES DE APOYO ---

def quitar(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto)
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def calculardesempeño(promedio):
    if promedio >= 4.5:
        return "Excelente"
    elif promedio >= 4:
        return "Bueno"
    elif promedio >= 3:
        return "Regular"
    else:
        return "Bajo"

# --- RUTAS DE FLASK ---

@app.route("/", methods=["GET", "POST"])
def login():
    if "UserName" in session:
        return redirect("/dashprincipal")

    if request.method == "POST":
        UserName = request.form.get("UserName")
        Password = request.form.get("Password")
        usuario = obtenerusuarios(UserName)

        if usuario and usuario["PasswordUser"] == Password:
            session["UserName"] = usuario["UserName"]
            session["rol"] = usuario["RolUsu"]
            return redirect("/dashprincipal")
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route("/dashprincipal") 
def dashprinci():
    if "UserName" not in session:
        return redirect("/")
    return render_template("dashprinci.html", usuario=session["UserName"])

@app.route("/registro", methods=["GET", "POST"])
def registroestudiantes():
    if "UserName" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            NombreEstu = request.form.get("NombreEstu")
            EdadEstu = request.form.get("EdadEstu")
            Carrera = request.form.get("Carrera")
            Nota1 = float(request.form.get("Nota1", 0))
            Nota2 = float(request.form.get("Nota2", 0))
            Nota3 = float(request.form.get("Nota3", 0))

            Promedio = round((Nota1 + Nota2 + Nota3) / 3, 2)
            # Nota: Desempeño se pasa como parámetro, la función insertar_estudiante 
            # se encarga de mapearlo a 'Desempeno' en la BD
            Desempeno = calculardesempeño(Promedio)
            
            insertar_estudiante(NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno)
            return redirect("/dashprincipal")
        except ValueError:
            return "Error: Las notas deben ser números."
    
    return render_template("RegistroEstudiante.html")

@app.route("/cargamasiva", methods=["GET", "POST"])
def cargamasiva():
    if "UserName" not in session:
        return redirect("/")

    if request.method == "POST":
        archivo = request.files.get("archivo")
        if not archivo:
            return "No se seleccionó ningún archivo"

        df = pd.read_excel(archivo)

        df.columns = df.columns.astype(str).str.strip()
        
        if 'idEstudiante' in df.columns:
            df = df.drop(columns=['idEstudiante'])

        # Limpieza de datos
        df["NombreEstu"] = df["NombreEstu"].astype(str).str.strip().apply(quitar).str.title()
        df["Carrera"] = df["Carrera"].astype(str).str.strip().apply(quitar).str.title()
        
        # Filtros de validación
        df = df[df["EdadEstu"] >= 0]
        for col in ["Nota1", "Nota2", "Nota3"]:
            df = df[(df[col] >= 0) & (df[col] <= 5)]

        df["Promedio"] = ((df["Nota1"] + df["Nota2"] + df["Nota3"]) / 3).round(2)
        df = df[df["Promedio"] <= 5]
        
        # IMPORTANTE: Aplicar la función que devuelve el string
        df["Desempeno"] = df["Promedio"].apply(calculardesempeño)

        df = df.drop_duplicates(subset=["NombreEstu", "Carrera"])

        # Inserción en la base de datos
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            # Usamos Desempeno (sin ñ) para coincidir con el SQL
            query = ("INSERT INTO estudiantes (NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            
            for _, row in df.iterrows():
                cursor.execute(query, (
                    row["NombreEstu"], row["EdadEstu"], row["Carrera"],
                    row["Nota1"], row["Nota2"], row["Nota3"],
                    row["Promedio"], row["Desempeno"]
                ))
            conn.commit()
            mensaje = f"Éxito: Se insertaron {len(df)} registros."
        except Exception as e:
            mensaje = f"Error al insertar: {e}"
        finally:
            conn.close() # Cerramos la conexión SIEMPRE al final

        return mensaje

    return render_template("carga_masiva.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)