import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ScraperService:
    """
    Service responsible for fetching and cleaning web page content.
    """

    def scrape_url(self, url: str) -> dict:
        """
        Downloads the page at the given URL and extracts its main text content.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; TechWatch-AI/1.0; +http://localhost)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Remove non-content tags to prevent indexing noise
            unwanted_tags = ["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]
            for tag in soup(unwanted_tags):
                tag.decompose()

            title = soup.title.string.strip() if soup.title else None

            raw_text = soup.get_text(separator=" ", strip=True)
            clean_text = " ".join(raw_text.split())

            logger.info("Successfully scraped %s (%d chars)", url, len(clean_text))

            return {
                "url": url,
                "title": title,
                "content": clean_text
            }

        except requests.RequestException as e:
            logger.error("Network error while scraping %s: %s", url, e)
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            logger.error("Parsing error for %s: %s", url, e)
            raise Exception(f"Failed to parse content: {str(e)}")