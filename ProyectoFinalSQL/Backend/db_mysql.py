# backend/db_mysql.py
from pymongo import MongoClient
import pymysql

def conectar_movies():
    client = MongoClient("mongodb://192.168.56.101:27017/")
    db = client["facolNoSql"]
    return db

#peliculas MONGO-------------
def obtener_peliculas(titulo=None, anio=None):
    db = conectar_movies()
    coleccion = db["movies"]
    query = {}

    if titulo and anio:
        try:
            query = {
                "titulo": {"$regex": titulo, "$options": "i"},
                "año": int(anio)
            }
        except ValueError:
            query = {"titulo": {"$regex": titulo, "$options": "i"}}
    elif titulo:
        query = {"titulo": {"$regex": titulo, "$options": "i"}}
    elif anio:
        try:
            query = {"año": int(anio)}
        except ValueError:
            query = {}

    return list(coleccion.find(query, {"_id": 0}))

#LIBROS MONGO
def obtener_libros(titulo=None, isbn=None, fecha=None, editorial=None):
    db = conectar_movies()
    coleccion = db["books"]
    query = {}

    if titulo and isinstance(titulo, str) and titulo.strip():
        query["title"] = {"$regex": titulo.strip(), "$options": "i"}

    if isbn and isinstance(isbn, str) and isbn.strip():
        query["isbn"] = isbn.strip()

    if fecha and isinstance(fecha, str) and fecha.strip():
        query["publication_date"] = fecha.strip()  # formato: "9/16/2006"

    if editorial and isinstance(editorial, str) and editorial.strip():
        query["publisher"] = {"$regex": editorial.strip(), "$options": "i"}

    return list(coleccion.find(query, {"_id": 0}))




def conectar():
    return pymysql.connect(
        host="192.168.56.101",
        user="root",
        password="sistemas2024",  # <-- asegúrate de que esto sea correcto
        database="nomina",
        cursorclass=pymysql.cursors.DictCursor
    )

def obtener_empleados():
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT codigo_empleado, nombre_empleado FROM Empleado")
            return cursor.fetchall()

def empleados_por_dependencia():
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT e.nombre_empleado, d.nombre_dependencia
                FROM Empleado e
                JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            """)
            return cursor.fetchall()

def empleados_con_cargo():
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT e.nombre_empleado, c.nombre_cargo
                FROM Empleado e
                JOIN Cargo c ON e.id_cargo = c.id_cargo
            """)
            return cursor.fetchall()

def empleados_incapacitados():
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT e.nombre_empleado, i.fecha_inicio, i.fecha_fin, i.tipo_incapacidad
                FROM Empleado e
                JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
                JOIN Incapacidad i ON n.id_novedad = i.id_novedad
            """)
            return cursor.fetchall()

def obtener_info_completa_empleado(codigo_empleado):
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    e.codigo_empleado, e.nombre_empleado, e.sueldo, 
                    c.nombre_cargo, d.nombre_dependencia,
                    eps.nombre_eps, arl.nombre_arl, p.nombre_pension,
                    n.dias_trabajados, n.bonificacion, n.transporte,
                    v.fecha_inicio AS vac_inicio, v.fecha_fin AS vac_fin,
                    i.fecha_inicio AS inc_inicio, i.fecha_fin AS inc_fin, i.tipo_incapacidad
                FROM Empleado e
                LEFT JOIN Cargo c ON e.id_cargo = c.id_cargo
                LEFT JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
                LEFT JOIN Eps eps ON e.id_eps = eps.id_eps
                LEFT JOIN Arl arl ON e.id_arl = arl.id_arl
                LEFT JOIN Pension p ON e.id_pension = p.id_pension
                LEFT JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
                LEFT JOIN Vacacion v ON n.id_novedad = v.id_novedad
                LEFT JOIN Incapacidad i ON n.id_novedad = i.id_novedad
                WHERE e.codigo_empleado = %s
            """, (codigo_empleado,))
            return cursor.fetchall()
