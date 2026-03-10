import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Article(Base):
    """
    SQLAlchemy model representing the 'articles' table.
    Shared with the Spring Boot orchestrator and includes pgvector support for semantic search.
    """
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    link = Column(String, unique=True, nullable=False)
    source_name = Column(String, name="source_name")
    pub_date = Column(DateTime, name="pub_date")
    full_content = Column(Text, name="full_content")
    created_at = Column(DateTime, name="created_at")

    # Vector embeddings (768 dimensions optimized for the nomic-embed-text model)
    embedding = Column(Vector(768), name="embedding")