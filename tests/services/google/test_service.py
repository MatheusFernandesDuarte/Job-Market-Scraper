# tests/services/google/test_service.py

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.core.filters.query_expander import QueryExpander
from src.models.job_model import JobPosting
from src.services.google.service import GoogleService


@pytest.fixture
def mock_client(mocker: MockerFixture) -> MagicMock:
    """Mocks the GoogleCseClient instance."""
    return mocker.patch("src.services.google.service.GoogleCseClient", autospec=True).return_value


@pytest.fixture
def mock_from_google_item(mocker: MockerFixture) -> MagicMock:
    """Mocks the from_google_cse_item mapper function."""
    return mocker.patch("src.services.google.service.from_google_cse_item")


@pytest.fixture
def mock_initial_filter(mocker: MockerFixture) -> MagicMock:
    """Mocks the InitialJobFilter class."""
    mock = mocker.patch("src.services.google.service.InitialJobFilter", autospec=True)
    mock.should_keep.return_value = True
    return mock


@pytest.fixture
def mock_expander(mocker: MockerFixture) -> MagicMock:
    """Mocks the QueryExpander instance."""
    mock = mocker.MagicMock(spec=QueryExpander)
    mock.expand.side_effect = lambda queries: queries
    return mock


@pytest.fixture
def sample_jobs() -> list[JobPosting]:
    """Provides a list of sample JobPosting objects."""
    return [
        JobPosting(title="Job 1", link="https://link1.com", snippet="a", source="a"),
        JobPosting(title="Job 2", link="https://link2.com", snippet="b", source="b"),
        JobPosting(title="Job 3", link="https://link3.com", snippet="c", source="c"),
    ]


def test_search_finds_enough_results_in_first_window(
    mock_client: MagicMock,
    mock_from_google_item: MagicMock,
    mock_initial_filter: MagicMock,
    mock_expander: MagicMock,
    sample_jobs: list[JobPosting],
) -> None:
    """Tests that the search stops after the first window if enough jobs are found."""
    mock_client.search.return_value = [{"raw": "item"}] * 3
    mock_from_google_item.side_effect = sample_jobs

    service = GoogleService(client=mock_client, expander=mock_expander)

    results = service.search(queries=["python"], max_results=3)

    assert len(results) == 3
    mock_client.search.assert_called_once()


def test_search_expands_window_when_needed(
    mock_client: MagicMock,
    mock_from_google_item: MagicMock,
    mock_initial_filter: MagicMock,
    mock_expander: MagicMock,
    sample_jobs: list[JobPosting],
) -> None:
    """Tests that the search continues to the next window if not enough jobs are found."""
    # First API call returns 1 item, second returns 2 more
    mock_client.search.side_effect = [[{"raw": "item"}], [{"raw": "item"}] * 2]
    mock_from_google_item.side_effect = sample_jobs  # Provides enough data for all calls

    service = GoogleService(client=mock_client, expander=mock_expander)

    results = service.search(queries=["python"], max_results=3)

    assert len(results) == 3
    assert mock_client.search.call_count == 2


def test_search_deduplicates_results(
    mock_client: MagicMock,
    mock_from_google_item: MagicMock,
    mock_initial_filter: MagicMock,
    mock_expander: MagicMock,
) -> None:
    """Tests that jobs with the same link are not duplicated across windows."""
    job_a = JobPosting(title="Job A", link="https://link-a.com", snippet="", source="")
    job_b = JobPosting(title="Job B", link="https://link-b.com", snippet="", source="")

    # Client will find 1 item in the first window, and 2 in the second
    mock_client.search.side_effect = [[{"raw": "a"}], [{"raw": "a"}, {"raw": "b"}]]
    # Mapper will return job_a, then job_a again, then job_b
    mock_from_google_item.side_effect = [job_a, job_a, job_b]

    service = GoogleService(client=mock_client, expander=mock_expander)

    results = service.search(queries=["python"], max_results=2)

    assert len(results) == 2
    assert {job.link for job in results} == {"https://link-a.com", "https://link-b.com"}
    assert mock_client.search.call_count == 2
