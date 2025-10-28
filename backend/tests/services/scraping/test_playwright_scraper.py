# backend/tests/services/scraping/test_playwright_scraper.py

from unittest.mock import ANY, AsyncMock, MagicMock

import pytest
from playwright.async_api import Error

from backend.src.services.scraping.playwright_scraper import PlaywrightScraper

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_playwright(mocker: MagicMock) -> dict:
    """
    Mocks the entire async Playwright chain, ensuring all awaitable
    methods are AsyncMocks.
    """
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()

    mock_browser.new_context = AsyncMock(return_value=mock_context)
    mock_browser.close = AsyncMock()

    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_context.close = AsyncMock()

    mock_page.route = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.content = AsyncMock(return_value="<html><body><h1>Scraped Content</h1></body></html>")

    playwright_instance_mock = MagicMock()
    playwright_instance_mock.chromium.launch = AsyncMock(return_value=mock_browser)
    playwright_instance_mock.stop = AsyncMock()

    mock_playwright_cm = mocker.patch("backend.src.services.scraping.playwright_scraper.async_playwright")
    mock_playwright_cm.return_value.start = AsyncMock(return_value=playwright_instance_mock)

    return {
        "playwright": playwright_instance_mock,
        "browser": mock_browser,
        "context": mock_context,
        "page": mock_page,
    }


async def test_context_manager_lifecycle(mock_playwright: dict) -> None:
    """Tests the async context manager lifecycle."""
    async with PlaywrightScraper():
        pass

    mock_playwright["browser"].close.assert_awaited_once()
    mock_playwright["playwright"].stop.assert_awaited_once()


async def test_fetch_content_success(mock_playwright: dict) -> None:
    """Tests the success path of fetching content."""
    mock_page = mock_playwright["page"]
    mock_context = mock_playwright["context"]

    async with PlaywrightScraper() as scraper:
        content = await scraper.fetch_content(url="http://fake-url.com")

    mock_page.route.assert_awaited_once_with(ANY, ANY)
    mock_page.goto.assert_awaited_once_with(url="http://fake-url.com", timeout=60000, wait_until="domcontentloaded")
    mock_context.close.assert_awaited_once()
    assert content == "Scraped Content"


async def test_fetch_content_handles_playwright_error(mock_playwright: dict) -> None:
    """Tests graceful failure when a Playwright error occurs."""
    mock_page = mock_playwright["page"]
    mock_context = mock_playwright["context"]
    mock_page.goto.side_effect = Error("Navigation timeout")

    async with PlaywrightScraper() as scraper:
        content = await scraper.fetch_content(url="http://failed-url.com")

    assert content == ""
    mock_context.close.assert_awaited_once()

