-- Crea una tabla para simular datos de sensores en el hogar
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY, -- Identificador único
    room VARCHAR(50) NOT NULL, -- Habitación donde está el sensor
    temperature NUMERIC(5, 2), -- Temperatura en grados Celsius
    energy_consumption NUMERIC(10, 2), -- Consumo energético en kWh
    co2_level NUMERIC(5, 2), -- Nivel de CO2 en ppm
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Marca de tiempo del dato
);

-- Inserta datos iniciales en la tabla 'sensors'
INSERT INTO sensors (room, temperature, energy_consumption, co2_level)
VALUES 
('Living Room', 22.5, 1.2, 450),
('Bedroom', 20.1, 0.8, 400),
('Kitchen', 25.3, 1.5, 500),
('Bathroom', 23.0, 0.5, 420),
('Garage', 18.7, 1.8, 480);

-- Crea índices para optimizar consultas
CREATE INDEX idx_room ON sensors(room);
CREATE INDEX idx_timestamp ON sensors(timestamp);

-- Visualización de la estructura y datos iniciales (opcional para depuración)
-- Esto solo funcionará si se ejecuta dentro de psql
-- SELECT * FROM sensors;
