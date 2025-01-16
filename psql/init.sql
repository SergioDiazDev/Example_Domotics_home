-- Tabla: Rooms
CREATE TABLE Rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tabla: Sensors
CREATE TABLE Sensors (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,  -- E.g., Temperature, Humidity, Light, etc.
    room_id INT REFERENCES Rooms(id) ON DELETE SET NULL
);

-- -- Tabla: Devices
-- CREATE TABLE Devices (
--     id SERIAL PRIMARY KEY,
--     type VARCHAR(50) NOT NULL, -- e.g., switch, light, radiator
--     state VARCHAR(20) DEFAULT 'OFF', -- ON/OFF or similar states
--     power_consumption DECIMAL, -- Consumption in watts/hour
--     room_id INT REFERENCES Rooms(id) ON DELETE SET NULL
-- );

-- Tabla: Sensor_Readings
CREATE TABLE Sensor_Readings (
    id SERIAL PRIMARY KEY,
    sensor_type VARCHAR(50) NOT NULL, -- 'Temperature', 'Humidity', 'Light'
    room_id INT REFERENCES Rooms(id) ON DELETE SET NULL,
    value DECIMAL NOT NULL,  -- Sensor reading value
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -- Tabla: Energy_Consumption
-- CREATE TABLE Energy_Consumption (
--     id SERIAL PRIMARY KEY,
--     device_id INT REFERENCES Devices(id) ON DELETE CASCADE,
--     energy_used DECIMAL NOT NULL,  -- Energy used in kWh
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Tabla: Solar_Production
-- CREATE TABLE Solar_Production (
--     id SERIAL PRIMARY KEY,
--     energy_generated DECIMAL NOT NULL, -- Energy generated in kWh
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Inserción de datos en la tabla Rooms
INSERT INTO Rooms (name) VALUES
('Living Room'), ('Kitchen'), ('Master Bedroom'), ('Secondary Bedroom'), ('Bathroom'), ('Office'), ('Garage'), ('Basement');

-- Inserción de datos en la tabla Sensors 
INSERT INTO Sensors (type, room_id)
SELECT 'Temperature', id FROM Rooms WHERE name IN ('Living Room', 'Kitchen', 'Master Bedroom', 'Bathroom', 'Secondary Bedroom', 'Office', 'Garage', 'Basement');

INSERT INTO Sensors (type, room_id)
SELECT 'Humidity', id FROM Rooms WHERE name IN ('Living Room', 'Kitchen', 'Master Bedroom', 'Bathroom', 'Secondary Bedroom', 'Office', 'Garage', 'Basement');

INSERT INTO Sensors (type, room_id)
SELECT 'Light', id FROM Rooms WHERE name IN ('Living Room', 'Kitchen', 'Master Bedroom', 'Bathroom', 'Secondary Bedroom', 'Office', 'Garage', 'Basement');

-- -- Inserción de datos en la tabla Devices
-- INSERT INTO Devices (type, state, power_consumption, room_id)
-- SELECT 'Light', 'OFF', 10, id FROM Rooms WHERE name IN ('Salón', 'Cocina', 'Dormitorio Principal', 'Dormitorio Secundario', 'Baño', 'Despacho', 'Comedor', 'Garaje', 'Sótano');

-- INSERT INTO Devices (type, state, power_consumption, room_id)
-- SELECT 'Radiator', 'OFF', 1500, id FROM Rooms WHERE name IN ('Salón', 'Dormitorio Principal','Despacho', 'Garaje', 'Sótano');

-- INSERT INTO Devices (type, state, power_consumption, room_id)
-- SELECT 'Air Conditioner', 'OFF', 1200, id FROM Rooms WHERE name IN ('Salón','Dormitorio Principal', 'Despacho', 'Garaje', 'Sótano');

-- INSERT INTO Devices (type, state, power_consumption, room_id)
-- SELECT 'Switch', 'OFF', 0, id FROM Rooms WHERE name IN ('Salón','Cocina','Dormitorio Principal', 'Dormitorio Secundario', 'Baño', 'Despacho', 'Comedor', 'Garaje', 'Sótano');

-- -- Inserción de datos en la tabla Energy_Consumption
-- INSERT INTO Energy_Consumption (device_id, energy_used, timestamp)
-- SELECT id, random() * (5 - 0.1) + 0.1, NOW() - INTERVAL '1 day' * i
-- FROM Devices, generate_series(0, 240, 1) AS i;

-- -- Inserción de datos en la tabla Solar_Production
-- INSERT INTO Solar_Production (energy_generated, timestamp)
-- SELECT random() * (10-0) + 0, NOW() - INTERVAL '1 day' * i
-- FROM generate_series(0, 240, 1) AS i;