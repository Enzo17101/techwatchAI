from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.schemas.scraping import ScrapeRequest, ScrapeResponse
from app.services.article_service import ArticleService
from app.services.rag_service import RagService
from app.services.scraper import ScraperService

router = APIRouter()
scraper_service = ScraperService()

@router.post("/scrape", response_model=ScrapeResponse)
def scrape_article(request: ScrapeRequest):
    """
    Extracts and cleans text content from a provided URL.
    """
    try:
        return scraper_service.scrape_url(str(request.url))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/articles/{article_id}/process")
def process_article(article_id: UUID, db: Session = Depends(get_db)):
    """
    Triggers web scraping and vector embedding generation for an existing article in the database.
    """
    service = ArticleService(db)
    updated_article = service.scrape_and_update_content(article_id)
    
    return {
        "id": updated_article.id,
        "title": updated_article.title,
        "content_length": len(updated_article.full_content or ""),
        "vector_generated": updated_article.embedding is not None,
        "status": "updated"
    }

@router.post("/chat")
def chat_with_rag(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Processes a user query through the RAG pipeline using semantic search 
    and returns the LLM-generated response.
    """
    service = RagService(db)
    answer = service.search_and_answer(request.question)
    
    return {"answer": answer}