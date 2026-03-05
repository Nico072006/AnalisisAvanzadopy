from flask import Flask,render_template,request,redirect,session
from database import obtenerusuarios
app =Flask (__name__)
from dashprincipal import creartablero

app.secret_key ="1070464999"
creartablero(app)
@app.route("/",methods=["GET","POST"])
def login():

    

    #Verificar si el formulario fue enviado
    if request.method=="POST":

        UserName =request.form["UserName"]
        Password =request.form["Password"]

        usuario = obtenerusuarios(UserName)

   

       
        #Verificar si existe 

        if usuario:
            if usuario["PasswordUser"] == Password:

                #Creo la sesion del usuario
                session ["UserName"]=usuario["UserName"]
                session ["rol"]=usuario["RolUsu"]
                return redirect("/dashprincipal/")
            else :
                return "Contraseña Incorrecta"
        else:
            return "Usuario no Existe"


    return render_template("login.html")


@app.route("/dashprincipal")
def dashprinci():
    if ("UserName") not in session:
        return redirect ("/")
    
    return render_template("dashprinci.html",usuario=session["UserName"])

if __name__=="__main__":
    app.run(debug=True)
