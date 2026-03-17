CREATE DATABASE IF NOT EXISTS asterisk;
USE asterisk;

CREATE TABLE IF NOT EXISTS cdr (
    uniqueid VARCHAR(150) NOT NULL,
    calldate DATETIME NOT NULL,
    src VARCHAR(80) NOT NULL,
    dst VARCHAR(80) NOT NULL,
    duration INT NOT NULL DEFAULT 0,
    billsec INT NOT NULL DEFAULT 0,
    disposition VARCHAR(45) NOT NULL DEFAULT '',
    PRIMARY KEY (uniqueid)
);

CREATE TABLE IF NOT EXISTS tarifas (
    id INT NOT NULL AUTO_INCREMENT,
    destino VARCHAR(32) NOT NULL,
    horario VARCHAR(32) NOT NULL,
    costo_por_minuto DECIMAL(10,4) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uniq_tarifa_destino_horario (destino, horario)
);

CREATE TABLE IF NOT EXISTS facturacion (
    id INT NOT NULL AUTO_INCREMENT,
    uniqueid VARCHAR(150) NOT NULL,
    src VARCHAR(80) NOT NULL,
    dst VARCHAR(80) NOT NULL,
    duracion INT NOT NULL DEFAULT 0,
    costo DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    fecha DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uniq_facturacion_uniqueid (uniqueid)
);
