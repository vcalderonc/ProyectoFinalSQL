# backend/db_mysql.py
from pymongo import MongoClient
import pymysql

def conectar_movies():
    client = MongoClient("mongodb://192.168.56.101:27017/")
    db = client["facolNoSql"]
    return db

#peliculas MONGO-------------
def obtener_peliculas(titulo=None, anio=None, genero=None):
    db = conectar_movies()
    coleccion = db["movies"]
    query = {}

    if titulo and titulo.strip():
        query["titulo"] = {"$regex": titulo.strip(), "$options": "i"}

    if anio:
        try:
            query["año"] = int(anio)
        except ValueError:
            pass

    # ⚠️ No filtramos por género, solo aceptamos el argumento para evitar el error
    print(">>> QUERY PELÍCULAS:", query)
    return list(coleccion.find(query, {"_id": 0}))

#LIBROS MONGO
def obtener_libros(titulo=None, isbn=None, editorial=None, autor=None, idioma=None, rating_min=None):
    db = conectar_movies()
    coleccion = db["books"]
    query = {}

    if titulo and titulo.strip():
        query["title"] = {"$regex": titulo.strip(), "$options": "i"}

    if isbn and isbn.strip():
        query["isbn"] = isbn.strip()

    if editorial and editorial.strip():
        query["publisher"] = {"$regex": editorial.strip(), "$options": "i"}

    if autor and autor.strip():
        query["authors"] = {"$regex": autor.strip(), "$options": "i"}

    if idioma and idioma.strip():
        query["language_code"] = idioma.strip()

    print(">>> QUERY FINAL (sin rating):", query)
    resultados = list(coleccion.find(query, {"_id": 0}))

    # Filtro de rating aplicado después de consultar Mongo
    if rating_min and rating_min.strip():
        try:
            rating_val = float(rating_min.strip())
            resultados_filtrados = []
            for libro in resultados:
                rating = libro.get("average_rating")
                try:
                    if rating is not None and float(rating) >= rating_val:
                        resultados_filtrados.append(libro)
                except ValueError:
                    continue  # ignora si el rating no es convertible
            resultados = resultados_filtrados
        except ValueError:
            print("⚠️ rating_min no es un número válido")


    return resultados



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
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT 
                e.codigo_empleado,
                e.nombre_empleado,
                e.apellido_empleado,
                e.fecha_ingreso,
                e.sueldo,
                c.nombre_cargo,
                d.nombre_dependencia,
                eps.nombre_eps,
                arl.nombre_arl,
                p.nombre_pension,
                n.dias_trabajados,
                n.bonificacion,
                n.transporte,
                v.fecha_inicio AS vac_inicio,
                v.fecha_fin AS vac_fin,
                i.fecha_inicio AS inc_inicio,
                i.fecha_fin AS inc_fin,
                i.tipo_incapacidad
            FROM Empleado e
            LEFT JOIN Cargo c ON e.id_cargo = c.id_cargo
            LEFT JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            LEFT JOIN Eps eps ON e.id_eps = eps.id_eps
            LEFT JOIN Arl arl ON e.id_arl = arl.id_arl
            LEFT JOIN Pension p ON e.id_pension = p.id_pension
            LEFT JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
            LEFT JOIN Vacacion v ON v.id_novedad = n.id_novedad
            LEFT JOIN Incapacidad i ON i.id_novedad = n.id_novedad
        """)
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
                    e.codigo_empleado, 
                    e.nombre_empleado, 
                    e.apellido_empleado,  -- ✅ SE AGREGA ESTA LÍNEA
                    e.sueldo, 
                    c.nombre_cargo, 
                    d.nombre_dependencia,
                    eps.nombre_eps, 
                    arl.nombre_arl, 
                    p.nombre_pension,
                    n.dias_trabajados, 
                    n.bonificacion, 
                    n.transporte,
                    v.fecha_inicio AS vac_inicio, 
                    v.fecha_fin AS vac_fin,
                    i.fecha_inicio AS inc_inicio, 
                    i.fecha_fin AS inc_fin, 
                    i.tipo_incapacidad
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

def empleados_por_rango_de_ingreso(desde, hasta):
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
                FROM Empleado e
                JOIN Cargo c ON e.id_cargo = c.id_cargo
                JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
                JOIN Eps eps ON e.id_eps = eps.id_eps
                JOIN Arl arl ON e.id_arl = arl.id_arl
                JOIN Pension p ON e.id_pension = p.id_pension
                WHERE e.fecha_ingreso BETWEEN %s AND %s
            """, (desde, hasta))
            return cursor.fetchall()
        

