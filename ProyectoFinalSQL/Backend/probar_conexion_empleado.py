# backend/probar_conexion.py

import pymysql

def conectar():
    return pymysql.connect(
        host="192.168.56.101",
        user="root",
        password="sistemas2024",  # <-- cambia esto
        database="nomina"
    )

try:
    conexion = conectar()
    print("✅ Conexión exitosa a la base de datos 'nomina'")
    conexion.close()
except Exception as e:
    print("❌ Error al conectar:", e)
