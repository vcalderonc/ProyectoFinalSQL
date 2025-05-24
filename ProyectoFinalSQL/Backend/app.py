from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


from db_mysql import (
    conectar,
    obtener_empleados,
    empleados_por_dependencia,
    empleados_con_cargo,
    empleados_incapacitados,
    obtener_info_completa_empleado,
    obtener_peliculas,
    obtener_libros
)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
# ----------------------------
# NoSql
# ----------------------------

@app.route("/libros", methods=["GET"])
def libros():
    titulo = request.args.get("titulo")
    isbn = request.args.get("isbn")
    fecha = request.args.get("fecha")
    editorial = request.args.get("editorial")
    resultado = obtener_libros(titulo, isbn, fecha, editorial)
    return render_template("libros.html", libros=resultado)


@app.route("/peliculas", methods=["GET"])
def peliculas():
    titulo = request.args.get("titulo")
    anio = request.args.get("anio")
   # genero = request.args.getlist("genero")
    resultado = obtener_peliculas(titulo, anio)
    return render_template("peliculas.html", peliculas=resultado)
# ----------------------------
# 
# ----------------------------



# SQL-------------------------

# ----------------------------
# Usuarios ficticios para login
# ----------------------------
usuarios = {
    "admin": {"clave": "admin123", "rol": "admin"},
    "empleado": {"clave": "emp123", "rol": "empleado"}
}
 


# ----------------------------
# Página principal
# ----------------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")

# ----------------------------
# Login
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        if usuario in usuarios and usuarios[usuario]["clave"] == clave:
            rol = usuarios[usuario]["rol"]
            if rol == "admin":
                return redirect(url_for("admin"))
            elif rol == "empleado":
                return redirect(url_for("empleado"))
        else:
            return render_template("inicio.html", error="Usuario o contraseña incorrectos.")

    return render_template("inicio.html")

# ----------------------------
# Panel de empleado
# ----------------------------
@app.route("/empleado")
def empleado():
    return render_template("empleado.html")


@app.route("/empleado/nomina_pdf")
def generar_pdf_nomina():
    codigo = request.args.get("codigo")
    if not codigo:
        return "Código de empleado requerido", 400

    datos = obtener_info_completa_empleado(codigo)
    if not datos:
        return "Empleado no encontrado", 404

    emp = datos[0]
    
    # Crear PDF en memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Nómina del Empleado")
    y -= 30

    p.setFont("Helvetica", 12)
    campos = [
        ("Código", emp["codigo_empleado"]),
        ("Nombre", emp["nombre_empleado"]),
        ("Cargo", emp["nombre_cargo"]),
        ("Dependencia", emp["nombre_dependencia"]),
        ("Sueldo", f"${emp['sueldo']}"),
        ("EPS", emp["nombre_eps"]),
        ("ARL", emp["nombre_arl"]),
        ("Pensión", emp["nombre_pension"]),
        ("Días trabajados", emp["dias_trabajados"]),
        ("Bonificación", f"${emp['bonificacion']}"),
        ("Transporte", f"${emp['transporte']}"),
        ("Vacaciones inicio", emp.get("vac_inicio", "-")),
        ("Vacaciones fin", emp.get("vac_fin", "-")),
        ("Incapacidad inicio", emp.get("inc_inicio", "-")),
        ("Incapacidad fin", emp.get("inc_fin", "-")),
        ("Tipo incapacidad", emp.get("tipo_incapacidad", "-")),
    ]

    for campo, valor in campos:
        p.drawString(50, y, f"{campo}: {valor}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=nomina_{codigo}.pdf"

    return response

# ----------------------------
# Panel de administrador con listas para el modal
# ----------------------------
@app.route("/admin")
def admin():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_eps, nombre_eps FROM Eps")
        eps = cursor.fetchall()

        cursor.execute("SELECT id_arl, nombre_arl FROM Arl")
        arl = cursor.fetchall()

        cursor.execute("SELECT id_pension, nombre_pension FROM Pension")
        pension = cursor.fetchall()

        cursor.execute("SELECT id_cargo, nombre_cargo FROM Cargo")
        cargos = cursor.fetchall()

        cursor.execute("SELECT id_dependencia, nombre_dependencia FROM Dependencia")
        dependencias = cursor.fetchall()

        cursor.execute("SELECT codigo_empleado, nombre_empleado FROM Empleado")
        empleados = cursor.fetchall()  # <-- Agrega esto

    return render_template("admin.html", eps=eps, arl=arl, pension=pension,cargos=cargos, dependencias=dependencias, empleados=empleados)
# ----------------------------
# Crear novedad desde modal
# ----------------------------
@app.route("/novedad/crear", methods=["POST"])
def crear_o_actualizar_novedad():
    datos = request.form
    codigo = datos["codigo"]

    dias = int(datos.get("dias") or 0)
    bono = float(datos.get("bono") or 0)
    transporte = float(datos.get("transporte") or 0)

    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_novedad FROM NovedadLaboral WHERE codigo_empleado = %s", (codigo,))
        novedad = cursor.fetchone()

        if novedad:
            # Actualizar (sumar) si ya existe novedad
            id_novedad = novedad["id_novedad"]
            cursor.execute("""
                UPDATE NovedadLaboral
                SET dias_trabajados = dias_trabajados + %s,
                    bonificacion = bonificacion + %s,
                    transporte = transporte + %s
                WHERE id_novedad = %s
            """, (dias, bono, transporte, id_novedad))
        else:
            # Insertar nueva novedad
            cursor.execute("""
                INSERT INTO NovedadLaboral (codigo_empleado, dias_trabajados, bonificacion, transporte)
                VALUES (%s, %s, %s, %s)
            """, (codigo, dias, bono, transporte))
            id_novedad = cursor.lastrowid

        # Vacaciones
        if datos.get("vac_inicio") and datos.get("vac_fin"):
            cursor.execute("""
                INSERT INTO Vacacion (id_novedad, fecha_inicio, fecha_fin, dias_vacaciones)
                VALUES (%s, %s, %s, DATEDIFF(%s, %s) + 1)
            """, (
                id_novedad,
                datos["vac_inicio"],
                datos["vac_fin"],
                datos["vac_fin"],
                datos["vac_inicio"]
            ))

        # Incapacidad
        if datos.get("inc_inicio") and datos.get("inc_fin"):
            cursor.execute("""
                INSERT INTO Incapacidad (id_novedad, fecha_inicio, fecha_fin, dias_incapacidad, tipo_incapacidad)
                VALUES (%s, %s, %s, DATEDIFF(%s, %s) + 1, %s)
            """, (
                id_novedad,
                datos["inc_inicio"],
                datos["inc_fin"],
                datos["inc_fin"],
                datos["inc_inicio"],
                datos.get("tipo_incapacidad")
            ))

    conexion.commit()
    return redirect(url_for("admin"))

# ----------------------------
# Crear empleado desde modal
# ----------------------------
@app.route("/empleado/crear", methods=["POST"])
def crear_empleado():
    datos = request.form
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Empleado (
                    codigo_empleado, nombre_empleado, apellido_empleado, id_dependencia, id_cargo, fecha_ingreso,
                    id_eps, id_arl, id_pension, sueldo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                datos["codigo"],
                datos["nombre"],
                datos["apellido"],
                datos["dependencia"],
                datos["cargo"],
                datos["fecha"],
                datos["eps"],
                datos["arl"],
                datos["pension"],
                datos["sueldo"]
            ))
        conexion.commit()
    return redirect(url_for("admin"))

# ----------------------------
# Eliminar empleado
# ----------------------------
@app.route("/empleado/eliminar", methods=["DELETE"])
def eliminar_empleado():
    codigo = request.args.get("codigo")
    if not codigo:
        return jsonify({"error": "Código requerido"}), 400

    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Empleado WHERE codigo_empleado = %s", (codigo,))
        conexion.commit()

    return jsonify({"mensaje": "Empleado eliminado correctamente"})
# ----------------------------
# EDITAR EMPLEADOS
# ----------------------------
@app.route("/empleado/actualizar", methods=["POST"])
def actualizar_empleado():
    datos = request.form
    conexion = conectar()
    with conexion:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE Empleado
                SET nombre_empleado = %s,
                    apellido_empleado = %s,
                    id_dependencia = %s,
                    id_cargo = %s,
                    fecha_ingreso = %s,
                    id_eps = %s,
                    id_arl = %s,
                    id_pension = %s,
                    sueldo = %s
                WHERE codigo_empleado = %s
            """, (
                datos["nombre"],
                datos["apellido"],
                datos["dependencia"],
                datos["cargo"],
                datos["fecha"],
                datos["eps"],
                datos["arl"],
                datos["pension"],
                datos["sueldo"],
                datos["codigo"]
            ))
        conexion.commit()
    return redirect(url_for("admin"))

# ----------------------------
# Consultas JSON de lectura
# ----------------------------
@app.route("/empleados", methods=["GET"])
def ver_empleados():
    return jsonify(obtener_empleados())

@app.route("/empleados/dependencia")
def ruta_empleados_por_dependencia():
    return jsonify(empleados_por_dependencia())

@app.route("/empleados/cargo")
def ruta_empleados_con_cargo():
    return jsonify(empleados_con_cargo())

@app.route("/empleados/incapacitados")
def ruta_empleados_incapacitados():
    return jsonify(empleados_incapacitados())

@app.route("/empleado/info", methods=["GET"])
def info_empleado():
    codigo = request.args.get("codigo")
    if not codigo:
        return jsonify({"error": "Se requiere el código del empleado"}), 400
    return jsonify(obtener_info_completa_empleado(codigo))

# ----------------------------
# Página extra
# ----------------------------
@app.route("/index")
def index():
    return render_template("index.html")



# ----------------------------
# Manejo de excepciones
# ---

# ----------------------------
# Ejecutar servidor
# ----------------------------



# ----------------------------
# Consultas JSON de lectura
# ----------------------------

@app.route("/admin/filtro/vacaciones")
def admin_filtro_vacaciones():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
            FROM Empleado e
            JOIN Cargo c ON e.id_cargo = c.id_cargo
            JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            JOIN Eps eps ON e.id_eps = eps.id_eps
            JOIN Arl arl ON e.id_arl = arl.id_arl
            JOIN Pension p ON e.id_pension = p.id_pension
            JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
            JOIN Vacacion v ON v.id_novedad = n.id_novedad
        """)
        return jsonify(cursor.fetchall())

@app.route("/admin/filtro/incapacidades")
def admin_filtro_incapacidades():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
            FROM Empleado e
            JOIN Cargo c ON e.id_cargo = c.id_cargo
            JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            JOIN Eps eps ON e.id_eps = eps.id_eps
            JOIN Arl arl ON e.id_arl = arl.id_arl
            JOIN Pension p ON e.id_pension = p.id_pension
            JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
            JOIN Incapacidad i ON i.id_novedad = n.id_novedad
        """)
        return jsonify(cursor.fetchall())

@app.route("/admin/filtro/sueldo")
def admin_filtro_sueldo():
    sueldo_min = request.args.get("min")
    if not sueldo_min:
        return jsonify({"error": "Parámetro 'min' requerido"}), 400

    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
            FROM Empleado e
            JOIN Cargo c ON e.id_cargo = c.id_cargo
            JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            JOIN Eps eps ON e.id_eps = eps.id_eps
            JOIN Arl arl ON e.id_arl = arl.id_arl
            JOIN Pension p ON e.id_pension = p.id_pension
            WHERE e.sueldo > %s
        """, (sueldo_min,))
        return jsonify(cursor.fetchall())

@app.route("/admin/filtro/combinar")
def admin_filtro_combinar():
    sueldo_min = request.args.get("min")
    incluir_vac = request.args.get("vac") == "1"
    incluir_inc = request.args.get("inc") == "1"

    query = """
        SELECT DISTINCT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
        FROM Empleado e
        JOIN Cargo c ON e.id_cargo = c.id_cargo
        JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
        JOIN Eps eps ON e.id_eps = eps.id_eps
        JOIN Arl arl ON e.id_arl = arl.id_arl
        JOIN Pension p ON e.id_pension = p.id_pension
        LEFT JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
        LEFT JOIN Vacacion v ON v.id_novedad = n.id_novedad
        LEFT JOIN Incapacidad i ON i.id_novedad = n.id_novedad
        WHERE 1 = 1
    """

    filtros = []
    valores = []

    if sueldo_min:
        filtros.append("e.sueldo > %s")
        valores.append(sueldo_min)

    if incluir_vac:
        filtros.append("v.id_vacacion IS NOT NULL")

    if incluir_inc:
        filtros.append("i.id_incapacidad IS NOT NULL")

    if filtros:
        query += " AND " + " AND ".join(filtros)

    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute(query, tuple(valores))
        return jsonify(cursor.fetchall())

@app.route("/admin/filtro/cargo")
def admin_filtro_por_cargo():
    id_cargo = request.args.get("id")
    if not id_cargo:
        return jsonify({"error": "Falta parámetro id"}), 400

    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT e.*, c.nombre_cargo, d.nombre_dependencia, eps.nombre_eps, arl.nombre_arl, p.nombre_pension
            FROM Empleado e
            JOIN Cargo c ON e.id_cargo = c.id_cargo
            JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
            JOIN Eps eps ON e.id_eps = eps.id_eps
            JOIN Arl arl ON e.id_arl = arl.id_arl
            JOIN Pension p ON e.id_pension = p.id_pension
            WHERE e.id_cargo = %s
        """, (id_cargo,))
        return jsonify(cursor.fetchall())
    
@app.route("/admin/filtro/fecha")
def admin_filtro_fecha():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if not desde or not hasta:
        return jsonify({"error": "Faltan parámetros 'desde' y 'hasta'"}), 400

    conexion = conectar()
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
        return jsonify(cursor.fetchall())

@app.route("/admin/filtro/avanzado")
def admin_filtro_avanzado():
    sueldo_min = request.args.get("sueldo")
    id_cargo = request.args.get("cargo")
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    incluir_vac = request.args.get("vac") == "1"
    incluir_inc = request.args.get("inc") == "1"

    query = """
        SELECT DISTINCT 
            e.codigo_empleado, e.nombre_empleado, e.apellido_empleado, e.sueldo, 
            c.nombre_cargo, d.nombre_dependencia,
            eps.nombre_eps, arl.nombre_arl, p.nombre_pension,
            v.fecha_inicio AS vac_inicio, v.fecha_fin AS vac_fin,
            i.fecha_inicio AS inc_inicio, i.fecha_fin AS inc_fin, i.tipo_incapacidad
        FROM Empleado e
        JOIN Cargo c ON e.id_cargo = c.id_cargo
        JOIN Dependencia d ON e.id_dependencia = d.id_dependencia
        JOIN Eps eps ON e.id_eps = eps.id_eps
        JOIN Arl arl ON e.id_arl = arl.id_arl
        JOIN Pension p ON e.id_pension = p.id_pension
        LEFT JOIN NovedadLaboral n ON e.codigo_empleado = n.codigo_empleado
        LEFT JOIN Vacacion v ON v.id_novedad = n.id_novedad
        LEFT JOIN Incapacidad i ON i.id_novedad = n.id_novedad
        WHERE 1 = 1
    """

    filtros = []
    valores = []

    if sueldo_min:
        filtros.append("e.sueldo > %s")
        valores.append(sueldo_min)

    if id_cargo:
        filtros.append("e.id_cargo = %s")
        valores.append(id_cargo)

    if desde and hasta:
        filtros.append("e.fecha_ingreso BETWEEN %s AND %s")
        valores.extend([desde, hasta])

    if incluir_vac:
        filtros.append("v.id_vacacion IS NOT NULL")

    if incluir_inc:
        filtros.append("i.id_incapacidad IS NOT NULL")

    if filtros:
        query += " AND " + " AND ".join(filtros)

    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute(query, tuple(valores))
        resultado = cursor.fetchall()

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)