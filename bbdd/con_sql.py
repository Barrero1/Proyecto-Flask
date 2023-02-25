import sqlite3 as sqlite
import os
def crear_tablas():
    """Crea base de datos y tabla

    Returns:None
    """
    conn = sqlite.connect('proyecto1.db') 
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
    (telefono TEXT PRIMARY KEY NOT NULL, nombre TEXT NOT NULL, password TEXT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS reservas 
    (telefono TEXT NOT NULL, ciudad TEXT NOT NULL, fecha_in DATE NOT NULL, fecha_out DATE NOT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS spotify 
    (id TEXT NOT NULL, name TEXT NOT NULL, artists TEXT NOT NULL, danceability FLOAT NOT NULL, 
    energy FLOAT NOT NULL, loudness FLOAT NOT NULL, speechiness FLOAT NOT NULL, acousticness FLOAT NOT NULL, 
    instrumentalness FLOAT NOT NULL, liveness FLOAT NOT NULL, valence FLOAT NOT NULL, tempo FLOAT NOT NULL,
    duration_ms INT NOT NULL, ranking INT NOT NULL, ranking_5 TEXT NOT NULL, cluster INT NOT NULL)''') 
    conn.close() 
    return None

def insertar_csv_spotify():
    import csv
    path = os.path.join('datos','spotify_cl.csv')
    try: # Lo intentamos
        con = sqlite.connect("proyecto1.db")
        cur = con.cursor()
        with open(path, 'r') as x:
            csv_reader = csv.reader(x)
            next(csv_reader) # Fila columnas
            for fila in csv_reader:
                cur.execute("INSERT OR IGNORE INTO spotify (id, name, artists, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, ranking,ranking_5, cluster) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], fila[12], fila[13], fila[14],fila[15]))
        con.commit()
    finally: # Pase lo que pase, cerramos la conexión
        con.close()


def artistas():
    con = sqlite.connect("proyecto1.db")
    cur = con.cursor()
    cur.execute("SELECT artists FROM spotify")
    a = cur.fetchall()
    con.close()
    return a


def insert_usuario(telefono:str, nombre:str, password:str) -> str:
    try: # Lo intentamos
        con = sqlite.connect("proyecto1.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (telefono, nombre, password) VALUES (?,?,?)",
        (telefono, nombre, password))
        con.commit()
        msg = True
    except: # Si no podemos insertar los datos en la base de datos
        con.rollback()
        msg = False
    finally: # Pase lo que pase, cerramos la conexión
        con.close()
    return msg


def insert_reserva(telefono:str, ciudad:str, fecha_in, fecha_out):
    try: # Lo intentamos
        con = sqlite.connect("proyecto1.db")
        cur = con.cursor()
        cur.execute("INSERT INTO reservas (telefono, ciudad, fecha_in, fecha_out) VALUES (?,?,?,?)",
        (telefono, ciudad, fecha_in, fecha_out))
        con.commit()
        return True
    except Exception as e: # Si no podemos insertar los datos en la base de datos
        con.rollback()
        return False
    finally: # Pase lo que pase, cerramos la conexión
        con.close()


def telefono_existe(telefono:str):
    con = sqlite.connect("proyecto1.db")
    cur = con.cursor()
    cur.execute("SELECT telefono FROM users WHERE telefono = ?", (telefono,)) 
    telefono_res = cur.fetchone()
    con.close()
    return telefono_res is not None

def comprobar_pwd(telefono:str, password:str):
    con = sqlite.connect("proyecto1.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE telefono = ?", (telefono,)) 
    pw = cur.fetchone()[0]
    con.close()
    return password == pw

def consultar_nombre(telefono:str):
    con = sqlite.connect("proyecto1.db")
    cur = con.cursor()
    cur.execute("SELECT nombre FROM users WHERE telefono = ?", (telefono,)) 
    nombre = cur.fetchone()[0]
    con.close()
    return nombre

def get_reservas(telefono):
    con = sqlite.connect("proyecto1.db")
    con.row_factory = sqlite.Row # 
    cur = con.cursor()
    cur.execute("SELECT ciudad, fecha_in, fecha_out FROM reservas WHERE telefono = ?", (telefono,)) 
    filas_bd = cur.fetchall() # Rows
    columnas_bd = [description[0] for description in cur.description] # Extraemos el nombre nombre de las columnas
    con.close()
    return filas_bd, columnas_bd
