import pandas as pd
import unicodedata 
from flask import Flask, render_template, request, redirect, session ,send_file
from database import conectar, obtenerusuarios, insertar_estudiante
from dashprincipal import creartablero
from database import obtenerestudiantes
import os

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

            #Eliminar y evitar usuarios duplicados
            df_actual= obtenerestudiantes()

            duplicado = df_actual[
                (df_actual["NombreEstu"].str.lower() == NombreEstu.lower()) & 
                (df_actual["Carrera"].str.lower() == Carrera.lower())
            ]

            if not duplicado.empty:
                return "<h1>El estudiante ya está registrado</h1>"


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

        df_original = pd.read_excel(archivo)
        df_original.columns = df_original.columns.astype(str).str.strip()

        # Contadores para las estadísticas
        insertados = 0
        rechazados = 0
        duplicados = 0
        
        registros_validos = []
        registros_finales_rechazados = [] # Para el Excel de errores

        df_bd = obtenerestudiantes()

        for _, row in df_original.iterrows():
            motivos = []
            es_duplicado = False

            # --- VALIDACIONES ---
            if row.isnull().any():
                motivos.append("Datos faltantes")
            
            try:
                if int(row.get("EdadEstu", -1)) < 0:
                    motivos.append("Edad negativa")
            except:
                motivos.append("Edad no válida")

            for n in ["Nota1", "Nota2", "Nota3"]:
                try:
                    valor = float(row.get(n, -1))
                    if valor < 0 or valor > 5:
                        motivos.append(f"{n} fuera de rango")
                except:
                    motivos.append(f"{n} no numérica")

            # --- VALIDAR DUPLICADOS ---
            nombre = quitar(str(row.get("NombreEstu", ""))).title().strip()
            carrera = quitar(str(row.get("Carrera", ""))).title().strip()
            
            if not df_bd.empty and nombre and carrera:
                if not df_bd[(df_bd["NombreEstu"] == nombre) & (df_bd["Carrera"] == carrera)].empty:
                    es_duplicado = True
                    motivos.append("Estudiante duplicado")

            # --- CLASIFICACIÓN PARA ESTADÍSTICAS ---
            if es_duplicado:
                duplicados += 1
            elif motivos: # Si tiene otros errores pero no es duplicado
                rechazados += 1
            else:
                insertados += 1

            # Guardar en la lista de errores si hubo cualquier motivo
            if motivos:
                fila_error = row.to_dict()
                fila_error["Motivo de Rechazo"] = " | ".join(motivos)
                registros_finales_rechazados.append(fila_error)
            else:
                # Preparar para insertar
                prom = round((float(row["Nota1"]) + float(row["Nota2"]) + float(row["Nota3"])) / 3, 2)
                registros_validos.append((nombre, row["EdadEstu"], carrera, row["Nota1"], row["Nota2"], row["Nota3"], prom, calculardesempeño(prom)))

        # 1. Guardar Excel de errores
        if registros_finales_rechazados:
            pd.DataFrame(registros_finales_rechazados).to_excel("estudiantes_rechazados.xlsx", index=False)

        # 2. Insertar válidos en la BD
        if registros_validos:
            conn = conectar()
            cursor = conn.cursor()
            query = "INSERT INTO estudiantes (NombreEstu, EdadEstu, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(query, registros_validos)
            conn.commit()
            conn.close()

        # 3. Retornar la tabla de estadísticas (PUNTO 4)
        return f"""
        <div style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Resumen del Proceso de Carga Masiva</h2>
            <table border="1" style="margin: 0 auto; border-collapse: collapse; width: 300px;">
                <tr style="background-color: #f2f2f2;">
                    <th>Resultado</th>
                    <th>Cantidad</th>
                </tr>
                <tr>
                    <td>Insertados</td>
                    <td style="color: green; font-weight: bold;">{insertados}</td>
                </tr>
                <tr>
                    <td>Rechazados</td>
                    <td style="color: red; font-weight: bold;">{rechazados}</td>
                </tr>
                <tr>
                    <td>Duplicados</td>
                    <td style="color: orange; font-weight: bold;">{duplicados}</td>
                </tr>
            </table>
            <br>
            <a href="/descargar_errores" style="background:red; color:white; padding:10px; text-decoration:none; border-radius:5px;">Descargar Errores</a>
            <br><br>
            <a href="/dashprincipal" style="color: blue;">Volver al Dashboard</a>
        </div>
        """

    return render_template("carga_masiva.html")


@app.route("/descargar_errores")
def descargar_errores():
    archivo_ruta = "estudiantes_rechazados.xlsx"
    
    # Verificamos si el archivo existe antes de intentar enviarlo
    if os.path.exists(archivo_ruta):
        return send_file(archivo_ruta, as_attachment=True)
    else:
        return "<h1>Error: El archivo de rechazados no existe o no se han generado errores aún.</h1>"


@app.route("/ranking")
def ranking():
    if "UserName" not in session:
        return redirect("/")

    #Obtener todos los estudiantes desde la BD
    df = obtenerestudiantes()

    if df.empty:
        return "<h1>Aún no hay estudiantes registrados para generar el ranking.</h1><br><a href='/dashprincipal'>Volver</a>"

    
    # Ordenamos de mayor a menor y tomamos 10
    top_10 = df.sort_values(by="Promedio", ascending=False).head(10)
    
    #Solo las columnas solicitadas
    ranking_data = top_10[["NombreEstu", "Carrera", "Promedio"]]

    #generamos tabla
    filas_tabla = ""
    for i, (_, row) in enumerate(ranking_data.iterrows(), 1):
        color_medalla = "#FFD900FF" if i == 1 else "#FFD900FF" if i == 2 else "#FFD900FF" if i == 3 else "#D31515DA"
        filas_tabla += f"""
            <tr style="background-color: {color_medalla if i <=3 else 'white'}">
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;"><b>{i}</b></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['NombreEstu']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['Carrera']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;"><b>{row['Promedio']}</b></td>
            </tr>
        """

    return f"""
    <div style="font-family: Arial; max-width: 800px; margin: 50px auto; text-align: center;">
        <h1 style="color: #000000FF;">🏆 Cuadro de Honor: Top 10 Estudiantes</h1>
        <table style="width: 100%; border-collapse: collapse; box-shadow: 0 0 20px rgba(0,0,0,0.1);">
            <thead>
                <tr style="background-color: #000000FF; color: white;">
                    <th style="padding: 10px;">Puesto</th>
                    <th style="padding: 10px;">Nombre del Estudiante</th>
                    <th style="padding: 10px;">Carrera</th>
                    <th style="padding: 10px;">Promedio</th>
                </tr>
            </thead>
            <tbody>
                {filas_tabla}
            </tbody>
        </table>
        <br>
        <a href="/dashprincipal" style="display: inline-block; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">
            Volver al Dashboard
        </a>
    </div>
    """


@app.route("/estudiantes_en_riesgo")
def estudiantes_en_riesgo():

    if "UserName" not in session:
        return redirect("/")

    df = obtenerestudiantes()

   
    df_riesgo = df[df["Promedio"] < 3.0]

    if df_riesgo.empty:
        return """
            <div style="text-align:center; margin-top:50px; font-family:Arial;">
                <h1 style="color:green;">✅ ¡Excelentes noticias!</h1>
                <p>No se encontraron estudiantes con promedio menor a 3.0.</p>
                <a href="/dashprincipal" style="color:blue;">Volver al Dashboard</a>
            </div>
        """

    # Generamos filas de la tabla
    filas = ""
    for _, row in df_riesgo.iterrows():
        filas += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['NombreEstu']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{row['Carrera']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; color: red; font-weight: bold;">{row['Promedio']}</td>
            </tr>
        """

    return f"""
    <div style="font-family: Arial; max-width: 700px; margin: 50px auto; text-align: center;">
        <h1 style="color: #D32F2F;">⚠️ Reporte de Estudiantes en Riesgo</h1>
        <p>Se consideran en riesgo por tener un promedio inferior a 3.0</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background-color: #D32F2F; color: white;">
                    <th style="padding: 12px;">Nombre</th>
                    <th style="padding: 12px;">Carrera</th>
                    <th style="padding: 12px;">Promedio</th>
                </tr>
            </thead>
            <tbody>
                {filas}
            </tbody>
        </table>
        <br>
        <p>Total de estudiantes en riesgo: <b>{len(df_riesgo)}</b></p>
        <a href="/dashprincipal" style="display: inline-block; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">
            Volver al Dashboard
        </a>
    </div>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)