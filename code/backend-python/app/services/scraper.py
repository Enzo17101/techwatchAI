import requests
from bs4 import BeautifulSoup
import logging

# Configure logger
logger = logging.getLogger(__name__)

class ScraperService:
    """
    Service responsible for fetching and cleaning web pages.
    """

    def scrape_url(self, url: str) -> dict:
        """
        Downloads the page and extracts useful text.
        """
        try:
            # 1. Fetch the page with a User-Agent to avoid being blocked
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; TechWatch-AI/1.0; +http://localhost)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for 4xx or 5xx errors

            # 2. Parse HTML with BeautifulSoup (using lxml for speed)
            soup = BeautifulSoup(response.content, "lxml")

            # 3. CLEANING: Remove unwanted tags (scripts, styles, navbars, footers)
            # This is crucial for RAG quality to avoid indexing Javascript code
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
                tag.decompose()  # Destroy the tag and its content

            # 4. Extract Title
            title = soup.title.string.strip() if soup.title else None

            # 5. Extract Text
            # get_text with separator ensures words don't stick together when tags are removed
            raw_text = soup.get_text(separator=" ", strip=True)

            # Basic cleanup of multiple spaces
            clean_text = " ".join(raw_text.split())

            logger.info(f"Successfully scraped {url} ({len(clean_text)} chars)")

            return {
                "url": url,
                "title": title,
                "content": clean_text
            }

        except requests.RequestException as e:
            logger.error(f"Network error while scraping {url}: {e}")
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            logger.error(f"Parsing error for {url}: {e}")
            raise Exception(f"Failed to parse content: {str(e)}")