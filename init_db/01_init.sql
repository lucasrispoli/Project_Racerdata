-- Script SQL de inicialização do PostgreSQL para o container
-- Tabelas do RACERDATA: session, driver, session_driver, dashboard_driver

CREATE TABLE IF NOT EXISTS session (
    id VARCHAR(36) PRIMARY KEY,
    session_key INTEGER NOT NULL UNIQUE,
    meeting_key INTEGER,
    session_name VARCHAR(100),
    session_type VARCHAR(50),
    year INTEGER,
    country_name VARCHAR(100),
    location VARCHAR(100),
    circuit_short_name VARCHAR(100),
    date_start VARCHAR(35),
    date_end VARCHAR(35),
    is_cancelled BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS driver (
    id VARCHAR(36) PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS session_driver (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL REFERENCES session(id) ON DELETE CASCADE,
    driver_id VARCHAR(36) NOT NULL REFERENCES driver(id) ON DELETE CASCADE,
    car_number INTEGER,
    team_name VARCHAR(100),
    CONSTRAINT uq_session_driver UNIQUE (session_id, driver_id)
);

CREATE TABLE IF NOT EXISTS dashboard_driver (
    id VARCHAR(36) PRIMARY KEY,
    driver_id VARCHAR(36) NOT NULL UNIQUE REFERENCES driver(id) ON DELETE CASCADE,
    description VARCHAR(255),
    tag_color VARCHAR(30) DEFAULT '#E10600',
    isActive BOOLEAN NOT NULL DEFAULT TRUE
);

-- Dados iniciais de demonstração
INSERT INTO driver (id, driver_name) VALUES
    ('d1000000-0000-0000-0000-000000000001', 'Lewis Hamilton'),
    ('d1000000-0000-0000-0000-000000000002', 'Max Verstappen'),
    ('d1000000-0000-0000-0000-000000000003', 'Charles Leclerc')
ON CONFLICT (driver_name) DO NOTHING;

INSERT INTO dashboard_driver (id, driver_id, description, tag_color, isActive) VALUES
    ('db100000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 'Heptacampeão Mundial de F1', '#00D2BE', true),
    ('db100000-0000-0000-0000-000000000002', 'd1000000-0000-0000-0000-000000000002', 'Tricampeão Mundial de F1', '#1E90FF', true),
    ('db100000-0000-0000-0000-000000000003', 'd1000000-0000-0000-0000-000000000003', 'Piloto Scuderia Ferrari', '#E10600', false)
ON CONFLICT (driver_id) DO NOTHING;
