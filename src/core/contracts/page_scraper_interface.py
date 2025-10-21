# src/core/contracts/page_scraper_interface.py

from abc import ABC, abstractmethod


class PageScraperInterface(ABC):
    """
    Abstract interface for a page scraper.

    This class defines the contract for any service that aims to fetch
    and parse the textual content from a given URL. It ensures that the
    application's core logic remains decoupled from specific scraping
    implementations (e.g., BeautifulSoup, Playwright).
    """

    @abstractmethod
    def fetch_content(self, url: str) -> str:
        """
        Fetches the content from a URL and returns its text.

        Args:
            url (str): The URL of the web page to scrape.

        Returns:
            str: The extracted plain text content of the page. Returns an
                 empty string if the page cannot be fetched or parsed.
        """
        pass
