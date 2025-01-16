import psycopg2
import time
import random
from datetime import datetime, timedelta
from threading import Thread, Event

# Configuración de la conexión a PostgreSQL
DB_HOST = "localhost"  # Ajusta según tu configuración
DB_NAME = "myHome"  # Reemplaza con el nombre de tu base de datos
DB_USER = "admin"  # Reemplaza con tu usuario
DB_PASSWORD = "admin123"  # Reemplaza con tu contraseña
DB_PORT = "5432" # Reemplaza con el puerto que estas usando

# Intervalo de tiempo entre inserciones de datos en segundos
INSERT_INTERVAL = 5

# Rangos para datos simulados
TEMP_RANGE = (15, 30)
HUMIDITY_RANGE = (30, 70)
LIGHT_RANGE = (0, 1000)
ENERGY_RANGE = (0.1, 5)
SOLAR_RANGE = (0, 10)

# Evento para detener los threads
stop_event = Event()

def get_rooms_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM Rooms;")
        return cur.fetchall()


def get_sensors_data(conn):
    with conn.cursor() as cur:
         cur.execute("SELECT id, type, room_id FROM Sensors;")
         return cur.fetchall()

def get_devices_data(conn):
    with conn.cursor() as cur:
         cur.execute("SELECT id FROM Devices;")
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


def insert_energy_consumption(conn, device_id, energy_used):
    try:
        with conn.cursor() as cur:
             cur.execute(
                """
                INSERT INTO Energy_Consumption (device_id, energy_used, timestamp)
                VALUES (%s, %s, NOW())
                """,
                (device_id, energy_used),
            )
             conn.commit()
    except Exception as e:
         print(f"Error inserting energy consumption: {e}")
         conn.rollback()


def insert_solar_production(conn, energy_generated):
     try:
        with conn.cursor() as cur:
            cur.execute(
                 """
                INSERT INTO Solar_Production (energy_generated, timestamp)
                VALUES (%s, NOW())
                """,
                (energy_generated,),
            )
            conn.commit()
     except Exception as e:
         print(f"Error inserting solar production: {e}")
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
                continue  # Skip if sensor type is unknown
            insert_sensor_reading(conn, sensor_type, room_id, value)
        time.sleep(INSERT_INTERVAL)


def simulate_energy_data(conn, devices, stop_event):
    while not stop_event.is_set():
        for device_id in devices:
            energy_used = round(random.uniform(*ENERGY_RANGE), 1)
            insert_energy_consumption(conn, device_id[0], energy_used)
        time.sleep(INSERT_INTERVAL)


def simulate_solar_data(conn, stop_event):
    while not stop_event.is_set():
        energy_generated = round(random.uniform(*SOLAR_RANGE), 1)
        insert_solar_production(conn, energy_generated)
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
        rooms = get_rooms_data(conn)
        sensors = get_sensors_data(conn)
        devices = get_devices_data(conn)
        # Inicia los threads
        sensor_thread = Thread(target=simulate_sensor_data, args=(conn, sensors, stop_event))
        energy_thread = Thread(target=simulate_energy_data, args=(conn, devices, stop_event))
        solar_thread = Thread(target=simulate_solar_data, args=(conn, stop_event))
        sensor_thread.start()
        energy_thread.start()
        solar_thread.start()
        print("Simulación de datos iniciada. Presiona Ctrl+C para detener.")
        # Mantiene el script principal ejecutándose hasta que se presione Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
        stop_event.set()  # Indica a los threads que se detengan
        sensor_thread.join()
        energy_thread.join()
        solar_thread.join()
        print("Simulación detenida.")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()