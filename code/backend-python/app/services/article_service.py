from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
import logging

from app.models.article import Article
from app.services.scraper import ScraperService
from app.services.ai_service import AiService

logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = ScraperService()
        self.ai_service = AiService()

    def scrape_and_update_content(self, article_id: UUID) -> Article:
        """
        1. Récupère l'article en base via son ID.
        2. Lance le scraping de l'URL.
        3. Génère l'embedding (Vecteur IA) avec Troncature Intelligente.
        4. Met à jour la base de données.
        """
        article = self.db.query(Article).filter(Article.id == article_id).first()

        if not article:
            logger.warning(f"Article {article_id} not found in DB")
            raise HTTPException(status_code=404, detail="Article not found")

        logger.info(f"Starting processing for article: {article.title}")
        try:
            # 1. Scraping du contenu web
            scrape_result = self.scraper.scrape_url(article.link)
            article.full_content = scrape_result["content"]

            # 2. Construction du texte pour l'IA (Titre + Desc + Contenu)
            # On donne un maximum de poids au début de l'article (Pyramide inversée)
            base_text = f"{article.title}. "
            if article.description:
                base_text += f"{article.description} "

            content_text = article.full_content or ""

            # Limite stricte de sécurité pour nomic-embed-text (par défaut ~8000 chars = ~2000 tokens)
            MAX_CHARS = 6500

            # Calcul de l'espace restant pour le contenu après avoir mis le titre et la description
            remaining_space = MAX_CHARS - len(base_text)

            text_to_vectorize = base_text

            if remaining_space > 0:
                # On prend la portion du contenu qui rentre
                chunk = content_text[:remaining_space]

                # TRONCATURE PROPRE : On évite de couper un mot au milieu
                # On cherche le dernier espace dans le chunk et on coupe là.
                if len(content_text) > remaining_space:
                    last_space_index = chunk.rfind(" ")
                    if last_space_index != -1:
                        chunk = chunk[:last_space_index]

                text_to_vectorize += chunk

            if len(article.full_content) > remaining_space and remaining_space > 0:
                logger.info(f"Text smartly truncated for AI ({len(content_text)} -> {len(chunk)} chars of content)")

            # 3. Appel à Ollama via LangChain
            vector = self.ai_service.generate_embedding(text_to_vectorize)
            article.embedding = vector

            # 4. Sauvegarde (Transaction DB)
            self.db.commit()
            self.db.refresh(article)

            logger.info(f"Article {article_id} updated successfully (Scraped + Vectorized)")
            return article

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to process article {article_id}: {e}")
            raise HTTPException(status_code=500, detail=str(e))