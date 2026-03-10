from pydantic import BaseModel, HttpUrl

class ScrapeRequest(BaseModel):
    """
    Input schema: The URL to scrape.
    HttpUrl ensures the string is a valid URL.
    """
    url: HttpUrl

class ScrapeResponse(BaseModel):
    """
    Output schema: The cleaned content.
    """
    url: str
    title: str | None = None
    content: str