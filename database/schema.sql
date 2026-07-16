CREATE DATABASE IF NOT EXISTS contract_sentinel;
USE contract_sentinel;

CREATE TABLE IF NOT EXISTS conversaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    documentos_fuente TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);