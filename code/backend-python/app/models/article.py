from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector  # <--- Import crucial
import uuid
from app.core.database import Base

class Article(Base):
    """
    Mirror of the 'articles' table created by Spring Boot (Java).
    Includes the vector column for AI.
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

    # Nouvelle colonne pour stocker le vecteur (768 dimensions pour nomic-embed-text)
    embedding = Column(Vector(768), name="embedding")