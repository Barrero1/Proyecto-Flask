import sqlite3 as sqlite

def crear_tablas():
    """Crea base de datos y tabla

    Returns:None
    """
    conn = sqlite.connect('database.db') 
    conn.execute('''CREATE TABLE IF NOT EXISTS usuarios 
    (email TEXT PRIMARY KEY NOT NULL, nombre TEXT NOT NULL, password TEXT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS reservas 
    (email TEXT NOT NULL, ciudad TEXT NOT NULL, fecha_in DATE NOT NULL, fecha_out DATE NOT NULL)''') 
    conn.close() 
    return None


def insert_usuario(email:str, nombre:str, password:str) -> str:
    try: # Lo intentamos
        con = sqlite.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (email, nombre, password) VALUES (?,?,?)",
        (email, nombre, password))
        con.commit()
        msg = True
    except: # Si no podemos insertar los datos en la base de datos
        con.rollback()
        msg = False
    finally: # Pase lo que pase, cerramos la conexión
        con.close()
    return msg


def insert_reserva(email:str, ciudad:str, fecha_in, fecha_out):
    try: # Lo intentamos
        con = sqlite.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO reservas (email, ciudad, fecha_in, fecha_out) VALUES (?,?,?,?)",
        (email, ciudad, fecha_in, fecha_out))
        con.commit()
        return True
    except Exception as e: # Si no podemos insertar los datos en la base de datos
        con.rollback()
        return False
    finally: # Pase lo que pase, cerramos la conexión
        con.close()


def email_existe(email:str):
    con = sqlite.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM usuarios WHERE email = ?", (email,)) 
    email_res = cur.fetchone()
    con.close()
    return email_res is not None

def comprobar_pwd(email:str, password:str):
    con = sqlite.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM usuarios WHERE email = ?", (email,)) 
    pw = cur.fetchone()[0]
    con.close()
    return password == pw

def consultar_nombre(email:str):
    con = sqlite.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT nombre FROM usuarios WHERE email = ?", (email,)) 
    nombre = cur.fetchone()[0]
    con.close()
    return nombre

def get_reservas(email):
    con = sqlite.connect("database.db")
    con.row_factory = sqlite.Row # 
    cur = con.cursor()
    cur.execute("SELECT ciudad, fecha_in, fecha_out FROM reservas WHERE email = ?", (email,)) 
    filas_bd = cur.fetchall() # Rows
    columnas_bd = [description[0] for description in cur.description] # Extraemos el nombre nombre de las columnas
    con.close()
    return filas_bd, columnas_bd
