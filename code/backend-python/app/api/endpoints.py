from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.schemas.scraping import ScrapeRequest, ScrapeResponse
from app.services.scraper import ScraperService
from app.services.article_service import ArticleService

from app.schemas.chat import ChatRequest
from app.services.rag_service import RagService

router = APIRouter()
scraper_service = ScraperService()

@router.post("/scrape", response_model=ScrapeResponse)
def scrape_article(request: ScrapeRequest):
    """
    Endpoint to scrape a URL.
    Receives a JSON { "url": "..." } and returns the cleaned text.
    """
    try:
        result = scraper_service.scrape_url(str(request.url))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/articles/{article_id}/process")
def process_article(article_id: UUID, db: Session = Depends(get_db)):
    """
    Déclenche le scraping et la sauvegarde pour un article donné existant en BDD.
    """
    service = ArticleService(db)
    updated_article = service.scrape_and_update_content(article_id)
    return {
        "id": updated_article.id,
        "title": updated_article.title,
        "content_length": len(updated_article.full_content or ""),
        # Petit ajout pour le monitoring :
        "vector_generated": updated_article.embedding is not None,
        "status": "updated"
    }


@router.post("/chat")
def chat_with_rag(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Reçoit une question du Frontend, interroge la base vectorielle,
    et retourne la réponse générée par l'IA (Gemma3).
    """
    service = RagService(db)
    answer = service.search_and_answer(request.question)

    # On retourne un JSON simple
    return {"answer": answer}