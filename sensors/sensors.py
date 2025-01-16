import psycopg2
import time
import random
from threading import Thread, Event
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Configuración de la conexión a PostgreSQL
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")

# Intervalo de tiempo entre inserciones de datos en segundos
INSERT_INTERVAL = 5

# Rangos para datos simulados
TEMP_RANGE = (0, 35)
HUMIDITY_RANGE = (0, 100)
LIGHT_RANGE = (0, 100)


# Evento para detener los threads
stop_event = Event()

def get_sensors_data(conn):
    with conn.cursor() as cur:
         cur.execute("SELECT id, type, room_id FROM Sensors;")
         return cur.fetchall()


def insert_sensor_reading(conn, sensor_type, room_id, value):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Sensor_Readings (sensor_type, room_id, value, timestamp)
                VALUES (%s, %s, %s, NOW())
                """,
                (sensor_type, room_id, value),
            )
            conn.commit()
    except Exception as e:
        print(f"Error inserting sensor reading: {e}")
        conn.rollback()


def simulate_sensor_data(conn, sensors, stop_event):
    while not stop_event.is_set():
        for sensor_id, sensor_type, room_id in sensors:
            if sensor_type == "Temperature":
                value = round(random.uniform(*TEMP_RANGE), 1)
            elif sensor_type == "Humidity":
                value = round(random.uniform(*HUMIDITY_RANGE), 1)
            elif sensor_type == "Light":
                value = round(random.uniform(*LIGHT_RANGE), 0)
            else:
                continue
            insert_sensor_reading(conn, sensor_type, room_id, value)
        time.sleep(INSERT_INTERVAL)


def main():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port = DB_PORT
        )
        sensors = get_sensors_data(conn)
        # Inicia los threads
        sensor_thread = Thread(target=simulate_sensor_data, args=(conn, sensors, stop_event))
        sensor_thread.start()
        print("Simulación de datos iniciada. Presiona Ctrl+C para detener.")
        # Mantiene el script principal ejecutándose hasta que se presione Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
        stop_event.set()  # Indica a los threads que se detengan
        sensor_thread.join()
        print("Simulación detenida.")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()