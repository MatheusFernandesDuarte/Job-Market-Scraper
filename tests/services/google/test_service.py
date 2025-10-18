"""
Unit tests for the GoogleService orchestrator.

This suite uses mocking to isolate the service from its dependencies (client,
filter) and verify its core business logic, including adaptive search,
error handling, and deduplication.
"""

from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from src.models.job_model import JobPosting
from src.services.google.client import GoogleCseClient
from src.services.google.service import GoogleService

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def mock_client(mocker: MockerFixture) -> MagicMock:
    """Provides a mock instance of the GoogleCseClient."""
    return mocker.MagicMock(spec=GoogleCseClient)


@pytest.fixture
def mock_filter(mocker: MockerFixture) -> MagicMock:
    """Provides a mock instance of the JobFilter."""
    mock = mocker.patch("src.services.google.service.JobFilter", autospec=True)
    return mock.return_value


@pytest.fixture
def sample_job_postings() -> list[JobPosting]:
    """Provides a list of sample JobPosting objects for mock responses."""
    return [
        JobPosting(title="Job 1", link="https://link1.com", snippet="", source=""),
        JobPosting(title="Job 2", link="https://link2.com", snippet="", source=""),
        JobPosting(title="Job 3", link="https://link3.com", snippet="", source=""),
    ]


# ==============================================================================
# Test Cases
# ==============================================================================


def test_search_finds_enough_results_in_first_window(
    mock_client: MagicMock,
    mock_filter: MagicMock,
    sample_job_postings: list[JobPosting],
) -> None:
    """
    Verify that the search stops after the first time window if enough
    results are found.
    """
    # ARRANGE
    mock_client.search.return_value = [{"title": "raw item"}]
    mock_filter.process.return_value = sample_job_postings  # Enough results

    service = GoogleService(client=mock_client)

    # ACT
    results: list[JobPosting] = service.search(queries=["python"], max_results=3)

    # ASSERT
    assert len(results) == 3
    mock_client.search.assert_called_once()  # Should only search the first window
    mock_filter.process.assert_called_once()


def test_search_expands_time_window_when_needed(
    mock_client: MagicMock,
    mock_filter: MagicMock,
    sample_job_postings: list[JobPosting],
) -> None:
    """
    Verify that the search continues to the next time window if the initial
    search does not yield enough results.
    """
    # ARRANGE
    # First call to filter returns too few, second call returns enough
    mock_filter.process.side_effect = [
        sample_job_postings[:1],  # 1 result
        sample_job_postings,  # 3 results
    ]
    mock_client.search.return_value = [{"title": "raw item"}]

    service = GoogleService(client=mock_client)

    # ACT
    results: list[JobPosting] = service.search(queries=["python"], max_results=3)

    # ASSERT
    assert len(results) == 3
    assert mock_client.search.call_count == 2  # Called for 7 and 14-day windows
    assert mock_filter.process.call_count == 2


def test_search_handles_api_errors_gracefully(
    mock_client: MagicMock,
    mock_filter: MagicMock,
    sample_job_postings: list[JobPosting],
) -> None:
    """
    Verify that a RequestException during a query does not stop the entire
    search process.
    """
    # ARRANGE
    mock_client.search.side_effect = [
        requests.RequestException("API Error"),  # First query fails
        [{"title": "raw item 2"}],  # Second query succeeds
    ]
    mock_filter.process.return_value = sample_job_postings

    service = GoogleService(client=mock_client)

    # ACT
    results: list[JobPosting] = service.search(queries=["q1", "q2"], max_results=3)

    # ASSERT
    assert len(results) == 3
    assert mock_client.search.call_count == 2  # Both queries were attempted


def test_search_deduplicates_results_across_windows(
    mock_client: MagicMock,
    mock_filter: MagicMock,
) -> None:
    """
    Verify that job postings with the same link are not duplicated, even if
    found in different time windows.
    """
    # ARRANGE
    # API returns the same item in two different searches
    raw_item = {"title": "Same Job", "link": "https://unique.com"}
    mock_client.search.return_value = [raw_item]

    # Filter returns one result, then two (one old, one new)
    job1 = JobPosting(title="Same Job", link="https://unique.com", snippet="", source="")
    job2 = JobPosting(title="New Job", link="https://new.com", snippet="", source="")
    mock_filter.process.side_effect = [[job1], [job1, job2]]

    service = GoogleService(client=mock_client)

    # ACT
    results: list[JobPosting] = service.search(queries=["python"], max_results=2)

    # ASSERT
    assert len(results) == 2
    assert results[0].link == "https://unique.com"
    assert results[1].link == "https://new.com"
    # The deduplication happens inside the loop, so the filter is still called twice
    assert mock_filter.process.call_count == 2


def test_search_returns_empty_list_when_no_results_found(
    mock_client: MagicMock,
    mock_filter: MagicMock,
) -> None:
    """
    Verify that an empty list is returned if no valid jobs are ever found.
    """
    # ARRANGE
    mock_client.search.return_value = []  # API returns nothing
    mock_filter.process.return_value = []  # Filter returns nothing

    service = GoogleService(client=mock_client)

    # ACT
    results: list[JobPosting] = service.search(queries=["python"], max_results=10)

    # ASSERT
    assert results == []
