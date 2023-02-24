from flask import Flask, render_template, request, session
import bbdd.con_sql as sql

sql.crear_tablas()

app = Flask(__name__)
app.secret_key = 'asdfDF92.,'


@app.route("/")
def home():
    return render_template('home.html')
        

@app.route("/reserva", methods = ["POST"])
def reserva():
    email = request.form.get("email")
    session['email'] = email
    password = request.form.get("password")
    if not sql.email_existe(email):
        return render_template('wrong_email.html')
    if not sql.comprobar_pwd(email, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(email)
    session['nombre'] = nombre
    return render_template('reserva.html', nombre = nombre)


@app.route("/gestion_reserva", methods = ["POST"])
def gestion_reserva():
    ciudad = request.form.get("ciudad")
    fecha_in = request.form.get("fecha_in")
    fecha_out = request.form.get("fecha_out")
    insertado = sql.insert_reserva(session['email'], ciudad, fecha_in, fecha_out)
    return render_template("reserva_realizada.html", insertado = insertado, nombre = session['nombre'])


@app.route("/get_reservas", methods = ["POST"])
def get_reservas():
    email = request.form.get("email")
    session['email'] = email
    password = request.form.get("password")
    if not sql.email_existe(email):
        return render_template('wrong_pwd.html')
    if not sql.comprobar_pwd(email, password):
        return render_template('wrong_pwd.html')
    nombre = sql.consultar_nombre(email)
    session['nombre'] = nombre
    filas_bd, columnas_bd = sql.get_reservas(session['email'])
    return render_template('tabla_reservas.html', nombre = nombre, columnas = columnas_bd, filas = filas_bd)


@app.route("/registro", methods = ["GET","POST"])
def registro():
    if request.method == "POST":
        email = request.form.get("email")
        nombre = request.form.get("nombre")
        password = request.form.get("password")
        insertado = sql.insert_usuario(email, nombre, password)
        return render_template("registro_completado.html", insertado = insertado)
    return render_template("registro.html")


if (__name__ == "__main__"):
    app.run(debug = True)