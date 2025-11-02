# backend/src/services/scraping/playwright_scraper.py

from __future__ import annotations

import logging

from bs4 import BeautifulSoup
from playwright.async_api import Browser, BrowserContext, Error, Page, Playwright, async_playwright
from readability import Document

from src.core.contracts.page_scraper_interface import PageScraperInterface

logger = logging.getLogger(__name__)


class PlaywrightScraper(PageScraperInterface):
    """
    An async, context-managed scraper using Playwright and BeautifulSoup.

    This class is designed to be used within an 'async with' statement. It
    launches a headless browser upon entering the context and closes it upon
    exiting, ensuring efficient reuse of the browser instance across multiple
    concurrent scraping tasks.
    """

    def __init__(self) -> None:
        """Initializes the scraper, setting browser and playwright to None."""
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def __aenter__(self) -> PlaywrightScraper:
        """
        Asynchronously starts the Playwright instance and launches the browser.

        Returns:
            PlaywrightScraper: The instance of the scraper itself.
        """
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Asynchronously closes the browser and stops the Playwright instance.
        """
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def fetch_content(self, url: str) -> str:
        """
        Asynchronously fetches page content in an isolated browser context.

        This high-performance version blocks non-essential resources like images
        and CSS. It also waits only until the DOM is loaded, not for all
        ancillary resources, resulting in a significantly faster scrape time.

        Args:
            url (str): The URL of the web page to scrape.

        Returns:
            str: The extracted plain text content of the page, or an empty string.
        """
        if not self._browser:
            raise RuntimeError("Browser is not running. Use this class within an 'async with' statement.")

        context: BrowserContext | None = None
        try:
            logger.info(f"Scraping URL: {url}")
            context: BrowserContext = await self._browser.new_context(
                java_script_enabled=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            )
            page: Page = await context.new_page()

            await page.route("**/*.{png,jpg,jpeg,css,woff,woff2,svg}", lambda route: route.abort())

            await page.goto(url=url, timeout=60000, wait_until="domcontentloaded")

            html_content: str = await page.content()
            doc = Document(html_content)
            clean_html: str = doc.summary()

            soup = BeautifulSoup(markup=clean_html, features="html.parser")
            return soup.get_text(separator=" ", strip=True)

        except Error as e:
            logger.warning(f"Playwright error fetching URL {url}: {e}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {e}", exc_info=False)
            return ""
        finally:
            if context:
                await context.close()
