import psycopg2
from datetime import datetime

# Configuración de conexión a PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "myHome"
DB_USER = "admin"
DB_PASSWORD = "admin123"

# Datos para insertar
room = "Office"
temperature = 21.8
energy_consumption = 0.9
co2_level = 420.5
timestamp = datetime.now()

try:
    # Establecer conexión
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # Crear cursor
    cursor = connection.cursor()

    # Consulta SQL para insertar datos
    insert_query = """
    INSERT INTO sensors (room, temperature, energy_consumption, co2_level, timestamp)
    VALUES (%s, %s, %s, %s, %s);
    """

    # Ejecutar consulta
    cursor.execute(insert_query, (room, temperature, energy_consumption, co2_level, timestamp))

    # Confirmar cambios
    connection.commit()

    print("Datos insertados correctamente en la tabla 'sensors'.")

except Exception as error:
    print(f"Error al insertar datos: {error}")

finally:
    # Cerrar conexión
    if connection:
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
