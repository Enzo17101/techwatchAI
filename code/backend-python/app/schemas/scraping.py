from pydantic import BaseModel, HttpUrl

class ScrapeRequest(BaseModel):
    """Payload for requesting text extraction from a specific URL."""
    url: HttpUrl

class ScrapeResponse(BaseModel):
    """Structured response containing the cleaned article content."""
    url: str
    title: str | None = None
    content: str