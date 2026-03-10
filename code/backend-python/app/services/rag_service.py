import logging
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.ai_service import AiService

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AiService()
        # Maximum character limit per article to prevent LLM context window overflow
        self.content_size = 4000

    def search_and_answer(self, question: str) -> str:
        """
        Executes the Retrieval-Augmented Generation (RAG) pipeline:
        Vectorizes the query, retrieves similar articles via pgvector,
        and generates a contextual answer using the LLM.
        """
        logger.info("Processing new RAG query: '%s'", question)

        logger.debug("Generating vector embedding for the user query...")
        question_vector = self.ai_service.generate_embedding(question)

        if not question_vector:
            return "I'm sorry, I couldn't process your question at this time."

        # Format vector for pgvector raw SQL compatibility
        vector_str = f"[{','.join(map(str, question_vector))}]"

        logger.debug("Performing semantic search in PostgreSQL...")

        # Retrieve the top 3 most relevant articles using L2 distance (<->)
        query = text("""
            SELECT title, source_name, full_content 
            FROM articles 
            WHERE embedding IS NOT NULL 
            ORDER BY embedding <-> :vector 
            LIMIT 3
        """)

        results = self.db.execute(query, {"vector": vector_str}).fetchall()

        if not results:
            logger.warning("No vectorized articles found in the database during semantic search.")
            return "My knowledge base is currently empty or indexing. Please try again later."

        logger.info("Found %d relevant articles. Building prompt context...", len(results))

        context = ""
        for row in results:
            title, source, content = row[0], row[1], row[2]

            # Enforce content truncation
            if content and len(content) > self.content_size:
                truncated_content = content[:self.content_size] + "..."
            else:
                truncated_content = content or ""

            context += f"\n--- Article: {title} (Source: {source}) ---\n"
            context += f"{truncated_content}\n"

        logger.debug("Requesting contextual answer generation from the LLM...")
        answer = self.ai_service.generate_answer(question, context)

        logger.info("RAG response generated successfully.")
        return answer