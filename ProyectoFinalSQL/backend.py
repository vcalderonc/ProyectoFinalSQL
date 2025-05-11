import mysql.connector
from mysql.connector import Error

try:
    # Establecer la conexión
    conexion = mysql.connector.connect(
        host='192.168.56.101',        
        user='root',       
        password='sistemas2024',
        database='Nomina'    
    )

    if conexion.is_connected():
        print("✅ Conexión exitosa a la base de datos")

        # Puedes ejecutar una consulta para probar
        cursor = conexion.cursor()
        cursor.execute("SELECT DATABASE();")
        nombre_bd = cursor.fetchone()
        print(f"📂 Base de datos actual: {nombre_bd[0]}")

except Error as e:
    print(f"❌ Error al conectar a la base de datos: {e}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("🔌 Conexión cerrada")
