from flask import Flask,render_template,request,redirect,session
from database import conectar
app =Flask (__name__)

@app.route("/",methods=["GET","POST"])
def login():

    #Verificar si el formulario fue enviado
    if request.method=="POST":

        UserName =request.form["UserName"]
        Password =request.form["Password"]

        #Conectar a la base bd

        conn =conectar()
        cursor=conn.cursor(dictionary=True)

        #Buscar el usuario en la bd

        cursor.execute("SELECT *FROM usuarios WHERE UserName=%s",(UserName))
        usuario =cursor.fetchone()
        conn.close()

        #Verificar si existe 

        if usuario:
            if usuario["Password"] == Password:

                #Creo la sesion del usuario
                session ["UserName"]=usuario["UserName"]
                session ["rol"]=usuario["rol"]
                return redirect("/")
            else :
                return "Contraseña Incorrecta"
        else:
            return "Usuario no Existe"


            return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
