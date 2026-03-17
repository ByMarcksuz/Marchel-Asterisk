USE asterisk;

INSERT INTO tarifas (destino, horario, costo_por_minuto)
VALUES
    ('nacional', 'normal', 0.0500),
    ('nacional', 'nocturno', 0.0300),
    ('internacional', 'normal', 0.1200),
    ('internacional', 'nocturno', 0.0900)
ON DUPLICATE KEY UPDATE costo_por_minuto = VALUES(costo_por_minuto);
