-- Enable the pgvector extension for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the main articles table supporting both metadata and vector embeddings
CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    link VARCHAR(1024) NOT NULL UNIQUE,
    source_name VARCHAR(255),
    pub_date TIMESTAMP,
    full_content TEXT,
    created_at TIMESTAMP,
    embedding vector(768)
);
