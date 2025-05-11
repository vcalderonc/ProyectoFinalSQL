from flask import Flask, render_template, jsonify, request
from db_mysql import (
    obtener_empleados,
    empleados_por_dependencia,
    empleados_con_cargo,
    empleados_incapacitados,
    obtener_info_completa_empleado
)

app = Flask(__name__, template_folder="../frontend/templates")

# Página principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Consultas básicas
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

# Consulta personalizada por código
@app.route("/empleado/info", methods=["GET"])
def info_empleado():
    codigo = request.args.get("codigo")
    if not codigo:
        return jsonify({"error": "Se requiere el código del empleado"}), 400
    return jsonify(obtener_info_completa_empleado(codigo))

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
