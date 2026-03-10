import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.article import Article
from app.services.ai_service import AiService
from app.services.scraper import ScraperService

logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = ScraperService()
        self.ai_service = AiService()

    def scrape_and_update_content(self, article_id: UUID) -> Article:
        """
        Executes the complete enrichment pipeline for a given article:
        Fetches metadata, scrapes full web content, generates vector embeddings 
        with smart truncation, and updates the database.
        """
        article = self.db.query(Article).filter(Article.id == article_id).first()

        if not article:
            logger.warning("Article %s not found in database.", article_id)
            raise HTTPException(status_code=404, detail="Article not found")

        logger.info("Starting processing pipeline for article: %s", article.title)
        
        try:
            # Scrape web content
            scrape_result = self.scraper.scrape_url(article.link)
            article.full_content = scrape_result.get("content", "")

            # Prepare text for vectorization
            # We prioritize the title and description (inverted pyramid structure)
            base_text = f"{article.title}. "
            if article.description:
                base_text += f"{article.description} "

            content_text = article.full_content or ""

            # Safety limit to avoid exceeding the embedding model's context window limits
            MAX_CHARS = 6500
            remaining_space = MAX_CHARS - len(base_text)

            text_to_vectorize = base_text
            chunk = ""

            if remaining_space > 0:
                chunk = content_text[:remaining_space]

                # Prevent word splitting during truncation
                if len(content_text) > remaining_space:
                    last_space_index = chunk.rfind(" ")
                    if last_space_index != -1:
                        chunk = chunk[:last_space_index]

                text_to_vectorize += chunk

            if len(content_text) > remaining_space and remaining_space > 0:
                logger.info("Content truncated for embedding window: %d -> %d characters.", len(content_text), len(chunk))

            # Generate embeddings
            vector = self.ai_service.generate_embedding(text_to_vectorize)
            article.embedding = vector

            # Commit transaction
            self.db.commit()
            self.db.refresh(article)

            logger.info("Article %s successfully processed and vectorized.", article_id)
            return article

        except Exception as e:
            self.db.rollback()
            logger.error("Failed to process article %s: %s", article_id, e)
            raise HTTPException(status_code=500, detail=str(e))