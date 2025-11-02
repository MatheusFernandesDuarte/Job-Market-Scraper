# backend/tests/core/use_cases/test_job_search_and_enrich_use_case.py

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.use_cases.job_search_and_enrich_use_case import JobSearchAndEnrichUseCase
from src.models.job_model import JobPosting

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_search_service() -> MagicMock:
    """Provides a mock for the JobSearchInterface."""
    return MagicMock()


@pytest.fixture
def mock_page_scraper() -> AsyncMock:
    """Provides an async mock for the PageScraperInterface."""
    scraper = AsyncMock()
    scraper.fetch_content.return_value = "A valid job description with requirements."
    return scraper


@pytest.fixture
def mock_initial_filter(mocker: MagicMock) -> MagicMock:
    """Mocks the InitialJobFilter to always return True."""
    return mocker.patch("backend.src.core.use_cases.job_search_and_enrich_use_case.InitialJobFilter.should_keep", return_value=True)


@pytest.fixture
def mock_job_validator(mocker: MagicMock) -> MagicMock:
    """Mocks the JobValidator to always return True."""
    return mocker.patch("backend.src.core.use_cases.job_search_and_enrich_use_case.JobValidator.is_valid", return_value=True)


async def test_execute_pipeline(
    mock_search_service: MagicMock,
    mock_page_scraper: AsyncMock,
    mock_initial_filter: MagicMock,
    mock_job_validator: MagicMock,
) -> None:
    """
    Tests that the execute method correctly orchestrates the full pipeline:
    search -> initial filter -> enrich -> final validation.
    """
    # Arrange: Create a pool of 15 candidate jobs
    initial_jobs = [JobPosting(title=f"Job {i}", link=f"http://test.com/{i}", snippet="", source="test") for i in range(15)]
    mock_search_service.search.return_value = initial_jobs

    use_case = JobSearchAndEnrichUseCase(
        search_service=mock_search_service,
        page_scraper=mock_page_scraper,
    )

    # Act: Execute the use case, asking for a final list of 5 jobs
    final_jobs = await use_case.execute(queries=["python"], max_results=5)

    # Assert
    # 1. Search was called to create a large pool
    use_case._search_service.search.assert_called_once_with(queries=["python"], max_results=use_case._CANDIDATE_POOL_SIZE)
    # 2. Initial filter was called for all candidates
    assert mock_initial_filter.call_count == 15

    # 3. Enrichment was only called for the first batch of 10
    assert mock_page_scraper.fetch_content.await_count == 10

    # 4. Validator was called on the enriched batch
    assert mock_job_validator.call_count == 10

    # 5. The final list has the desired size
    assert len(final_jobs) == 5
