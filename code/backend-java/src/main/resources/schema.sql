-- 1. On nettoie pour être sûr de repartir sur une base saine
DROP TABLE IF EXISTS articles;

-- 2. Activer l'extension vectorielle
-- 3. Créer la table avec TOUTES les colonnes (Java + Python)
CREATE TABLE articles (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    link VARCHAR(1024) NOT NULL UNIQUE,
    source_name VARCHAR(255),
    pub_date TIMESTAMP,
    full_content TEXT,
    created_at TIMESTAMP,
    embedding vector(768) -- La colonne critique pour l'IA
);