from flask import Flask, render_template, request, redirect, url_for, jsonify
from db_mysql import (
    conectar,
    obtener_empleados,
    empleados_por_dependencia,
    empleados_con_cargo,
    empleados_incapacitados,
    obtener_info_completa_empleado
)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

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
            return render_template("login.html", error="Usuario o contraseña incorrectos.")

    return render_template("login.html")

# ----------------------------
# Panel de empleado
# ----------------------------
@app.route("/empleado")
def empleado():
    return render_template("empleado.html")

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

    return render_template("admin.html", eps=eps, arl=arl, pension=pension, cargos=cargos, dependencias=dependencias)

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
# Ejecutar servidor
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
