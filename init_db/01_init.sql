-- Script SQL de inicialização do PostgreSQL para o container
-- Cria a tabela driver com os atributos: id, name, description, active

CREATE TABLE IF NOT EXISTS driver (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE
);
