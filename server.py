from flask import Flask, render_template, request, session
import bbdd.con_sql as sql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

sql.crear_tablas()
sql.insertar_csv_spotify()
datos = sql.spotify()
datos_num = sql.numericas(datos)

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
        return render_template('telefono_incorrecto.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono)
    session['nombre'] = nombre
    artistas = sql.pd_artistas(datos)
    return render_template('reserva.html', nombre = nombre, artistas=artistas)

@app.route("/grafico",methods = ["POST"])
def grafico():
    telefono = request.form.get("telefono")
    session['telefono'] = telefono
    password = request.form.get("password")
    if not sql.telefono_existe(telefono):
        return render_template('telefono_incorrecto.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono)
    session['nombre'] = nombre

    return render_template('grafico_formulario.html', nombre = nombre)    
    

@app.route("/grafico_variables",methods = ["POST"])
def grafico_variables():
    grafico = request.form.get('grafico')
    session['grafico'] = grafico
    if grafico == 'pointplot':
        var = range(2)
    else:
        var = range(1)
    variables = datos_num.columns.tolist()
    return render_template('grafico_variables.html',num_variables =var, nombre= session['nombre'], variables = variables, grafico = session['grafico'])

@app.route("/grafico_imagen",methods = ["POST"])
def grafico_imagen():
    grafico = request.form.get('grafico')
    session['grafico'] = grafico
    if grafico == 'pointplot':
        pass
    elif grafico == 'histogram':
        pass
    elif grafico == 'boxplot':
        pass
    return render_template('grafico_imagen.html', nombre= session['nombre'], grafico = session['grafico'])

@app.route("/gestion_artista", methods = ["POST"])
def gestion_artista():
    artista = request.form.get("artista")
    insertado = sql.insert_artista(session['telefono'], artista)
    return render_template("artista_seleccionado.html", insertado = insertado, nombre = session['nombre'])


@app.route("/get_artistas", methods = ["POST"])
def get_artistas():
    telefono = request.form.get("telefono")
    session['telefono'] = telefono
    password = request.form.get("password")
    if not sql.telefono_existe(telefono):
        return render_template('telefono_incorrecto.html')
    if not sql.comprobar_pwd(telefono, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(telefono) 
    session['nombre'] = nombre
    filas_bd, columnas_bd = sql.get_artistas(session['telefono'])
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