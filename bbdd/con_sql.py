import sqlite3 as sqlite
import os
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
def crear_tablas():
    """Crea base de datos y tabla

    Returns:None
    """
    conn = sqlite.connect('proyecto1.db') 
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
    (telefono TEXT PRIMARY KEY NOT NULL, nombre TEXT NOT NULL, password TEXT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS artistas 
    (telefono TEXT NOT NULL, artista TEXT NOT NULL, fecha DATE NOT NULL)''') 
    ################################################################################
    # conn.execute('''CREATE TABLE IF NOT EXISTS spotify 
    # (id TEXT NOT NULL, name TEXT NOT NULL, artists TEXT NOT NULL, danceability FLOAT NOT NULL, 
    # energy FLOAT NOT NULL, loudness FLOAT NOT NULL, speechiness FLOAT NOT NULL, acousticness FLOAT NOT NULL, 
    # instrumentalness FLOAT NOT NULL, liveness FLOAT NOT NULL, valence FLOAT NOT NULL, tempo FLOAT NOT NULL,
    # duration_ms INT NOT NULL, ranking INT NOT NULL, ranking_5 TEXT NOT NULL, cluster INT NOT NULL)''') 
    conn.close() 
    return None

################################################################################
# def insertar_csv_spotify():
#     import csv
#     path = os.path.join('datos','spotify_cl.csv')
#     try: # Lo intentamos
#         con = sqlite.connect("proyecto1.db")
#         cur = con.cursor()
#         with open(path, 'r') as x:
#             csv_reader = csv.reader(x)
#             next(csv_reader) # Fila columnas
#             for fila in csv_reader:
#                 cur.execute("INSERT OR IGNORE INTO spotify (id, name, artists, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, ranking,ranking_5, cluster) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                 (fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], fila[12], fila[13], fila[14],fila[15]))
#         con.commit()
#     finally: # Pase lo que pase, cerramos la conexión
#         con.close()
# def artistas():
#     con = sqlite.connect("proyecto1.db")
#     cur = con.cursor()
#     cur.execute("SELECT artists FROM spotify")
#     a = cur.fetchall()
#     con.close()
#     return a
########################################################################################################################


def spotify():
    path = os.path.join('datos','spotify_cl.csv')
    datos = pd.read_csv(path)
    return datos
    
def pd_artistas(df):
    artistas = df['artists'].replace(' ', '_', regex=True)
    return artistas

def numericas(df):
    cols_numericas = df.select_dtypes(include=np.number).columns.tolist()
    cols_numericas = cols_numericas[:-2]# quitar cluster y ranking que no interesa mucho verlo 
    df_numericas = df[cols_numericas]
    return df_numericas




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


def insert_artista(telefono:str, artista:str):
    try: # Lo intentamos
        con = sqlite.connect("proyecto1.db")
        cur = con.cursor()
        #fecha = datetime.datetime.now().replace(second=0, microsecond=0)
        #fecha = fecha.round(datetime.timedelta(hours=1))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO artistas (telefono, artista, fecha) VALUES (?,?,?)",
        (telefono, artista, fecha))
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

def get_artistas(telefono):
    con = sqlite.connect("proyecto1.db")
    con.row_factory = sqlite.Row # 
    cur = con.cursor()
    cur.execute("SELECT artista, fecha FROM artistas WHERE telefono = ?", (telefono,)) 
    filas_bd = cur.fetchall() # Rows
    columnas_bd = [description[0] for description in cur.description] # Extraemos el nombre nombre de las columnas
    con.close()
    return filas_bd, columnas_bd


###### ESTOY SEGURO QUE HAY UNA MANERA DE CONSEGUIR JUNTAR ESTAS FUNCIONES DE ABAJO PERO NO LO HE CONSEGUIDO 
datos = spotify()
def graficos_hist(columna:str):
    """Esta función devuelve un histograma de densidad del la columna indicada

    Args:
        columna (str): columna del dataframe (columna tipo numérica)

    Returns:
        path: Path donde se va a guardar el grafico en formato png
    """
    titulo = 'Boxplot de las columna '+columna
    fig = sns.distplot(datos[columna], hist=True, kde=True, color='green').set(title=titulo)
    plt.savefig('./static/imagenes/histograma_'+columna+'.png')
    path = './static/imagenes/histograma_'+columna+'.png'
    #Guardo el path para que cuando ejecute el siguiente html me salga la imagen en la pantalla
    return path 

def graficos_boxplot(columna:str):
    """Esta función devuelve un boxplot de la columna indicada

    Args:
        columna (str): columna del dataframe (columna tipo numérica)

    Returns:
        path: Path donde se va a guardar el grafico en formato png
    """
    titulo = 'Boxplot de las columna '+columna
    fig = sns.boxplot(datos[columna],color='green',palette="Set3", linewidth=2.5,width=0.3).set(title=titulo)
    plt.savefig('./static/imagenes/boxplot_'+columna+'.png')
    path = './static/imagenes/boxplot_'+columna+'.png'
    #Guardo el path para que cuando ejecute el siguiente html me salga la imagen en la pantalla
    return path 

def graficos_scatterplot(columna:str,columna2:str):
    """Esta función devuelve un scatter de las columnas indicadas

    Args:
        columna1 (str): columna del dataframe (columna tipo numérica)
        columna2 (str): columna del dataframe (columna tipo numérica)

    Returns:
        plot: histograma de densidad
    """
    titulo = 'Pointplot de las columnas '+columna+' y '+columna2
    fig = sns.scatterplot(x= datos[columna],y = datos[columna2],color = 'lightgreen',palette="Set2", edgecolor="gray", alpha=0.8, s=80).set(title=titulo)
    plt.savefig('./static/imagenes/scatter_'+columna+'_y_'+columna2+'.png')
    path = './static/imagenes/scatter_'+columna+'_y_'+columna2+'.png'
    #Guardo el path para que cuando ejecute el siguiente html me salga la imagen en la pantalla
    return path 

def limpiar_carpeta_graficos():
    carpeta = './static/imagenes/'
    # Jugar con esta aplicacion puede crear muchos graficos 
    # diferentes que pueden acabar ocupando mucho espacio
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
    return None