from flask import Flask, render_template, request, session
import bbdd.con_sql as sql
import pandas as pd
sql.crear_tablas()
sql.insertar_csv_spotify()
app = Flask(__name__)
app.secret_key = 'Australopitecus'


@app.route("/")
def home():
    return render_template('home.html')
        

@app.route("/artistas", methods = ["POST"])
def artistas():
    telefono = request.form.get("telefono")
    session['telefono'] = telefono
    password = request.form.get("password")
    if not sql.telefono_existe(telefono):
        return render_template('wrong_email.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono)
    session['nombre'] = nombre
    artistas = sql.artistas()
    return render_template('reserva.html', nombre = nombre, artistas=artistas)

@app.route("/grafico",methods = ["POST"])
def grafico():
    telefono = request.form.get("telefono")
    session['telefono'] = telefono
    password = request.form.get("password")
    if not sql.telefono_existe(telefono):
        return render_template('wrong_email.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono)
    session['nombre'] = nombre
    artistas = sql.artistas()
    return render_template('grafico_formulario.html', nombre = nombre)    
    

@app.route("/grafico_variables",methods = ["POST"])
def grafico_variables():
    grafico = request.form.get('grafico')
    session['grafico'] = grafico
    if grafico == 'pointplot':
        var = 2
    else:
        var = 1
    return render_template('grafico_variables',variables =var, nombre= session['nombre'])
    pass

@app.route("/gestion_reserva", methods = ["POST"])
def gestion_reserva():
    ciudad = request.form.get("ciudad")
    fecha_in = request.form.get("fecha_in")
    fecha_out = request.form.get("fecha_out")
    insertado = sql.insert_reserva(session['telefono'], ciudad, fecha_in, fecha_out)
    return render_template("reserva_realizada.html", insertado = insertado, nombre = session['nombre'])


@app.route("/get_reservas", methods = ["POST"])
def get_reservas():
    telefono = request.form.get("telefono")
    session['telefono'] = telefono
    password = request.form.get("password")
    if not sql.telefono_existe(telefono):
        return render_template('wrong_email.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono) 
    session['nombre'] = nombre
    filas_bd, columnas_bd = sql.get_reservas(session['telefono'])
    return render_template('tabla_reservas.html', nombre = nombre, columnas = columnas_bd, filas = filas_bd)


@app.route("/registro", methods = ["GET","POST"])
def registro():
    if request.method == "POST":
        telefono = request.form.get("telefono")
        nombre = request.form.get("nombre")
        password = request.form.get("password")
        insertado = sql.insert_usuario(telefono, nombre, password)
        return render_template("registro_completado.html", insertado = insertado)
    return render_template("registro.html")


if (__name__ == "__main__"):
    app.run(debug = True)