"""
Unit tests for the GoogleCseClient.

This suite uses mocking to isolate the client from the network and environment,
allowing for fast and reliable testing of its logic.
"""

from typing import Any
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from src.services.google.client import GoogleCseClient

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fixture to set the necessary environment variables for the client."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_api_key")
    monkeypatch.setenv("GOOGLE_CX", "test_cx_id")


@pytest.fixture
def mock_api_response() -> dict[str, Any]:
    """A fixture providing a sample successful API response."""
    return {
        "items": [
            {"title": "Test Job 1", "link": "https://example.com/1"},
            {"title": "Test Job 2", "link": "https://example.com/2"},
        ]
    }


# ==============================================================================
# Initialization Tests
# ==============================================================================


def test_google_cse_client_initialization_success(mock_env_vars: None) -> None:
    """
    Verify that the GoogleCseClient initializes correctly when all
    environment variables are present.
    """
    # ACT
    try:
        client = GoogleCseClient()
        # ASSERT
        assert client.api_key == "test_api_key"
        assert client.cx == "test_cx_id"
    except RuntimeError:
        pytest.fail("RuntimeError should not be raised when env vars are set.")


def test_google_cse_client_initialization_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Verify that the GoogleCseClient raises a RuntimeError if environment
    variables are missing.
    """
    # ARRANGE: Ensure environment variables are not set
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_CX", raising=False)

    # ACT & ASSERT
    with pytest.raises(RuntimeError, match="Missing GOOGLE_API_KEY or GOOGLE_CX"):
        GoogleCseClient()


# ==============================================================================
# Search Method Tests
# ==============================================================================


def test_search_success_without_date_filter(
    mocker: MockerFixture,
    mock_env_vars: None,
    mock_api_response: dict[str, Any],
) -> None:
    """
    Verify the search method correctly calls the API and returns items
    when no date filter is provided.
    """
    # ARRANGE
    mock_response = MagicMock()
    mock_response.json.return_value = mock_api_response
    mock_get = mocker.patch("requests.Session.get", return_value=mock_response)

    client = GoogleCseClient()
    query = "python developer"

    # ACT
    results: list[dict] = client.search(query=query)

    # ASSERT
    assert results == mock_api_response["items"]
    mock_get.assert_called_once()
    call_args, call_kwargs = mock_get.call_args
    assert "params" in call_kwargs
    assert call_kwargs["params"]["q"] == query
    assert "dateRestrict" not in call_kwargs["params"]


@pytest.mark.parametrize(
    "date_filter_input, expected_date_restrict",
    [
        ("qdr:d", "d1"),
        ("qdr:w", "w1"),
        ("qdr:m", "m1"),
    ],
)
def test_search_with_valid_date_filter(
    mocker: MockerFixture,
    mock_env_vars: None,
    date_filter_input: str,
    expected_date_restrict: str,
) -> None:
    """

    Verify the search method correctly adds the 'dateRestrict' parameter
    for valid date filters.
    """
    # ARRANGE
    mock_get = mocker.patch("requests.Session.get")
    client = GoogleCseClient()

    # ACT
    client.search(query="test", date_filter=date_filter_input)

    # ASSERT
    mock_get.assert_called_once()
    _, call_kwargs = mock_get.call_args
    assert call_kwargs["params"]["dateRestrict"] == expected_date_restrict


def test_search_with_invalid_date_filter(mocker: MockerFixture, mock_env_vars: None) -> None:
    """
    Verify that an invalid date filter is ignored and 'dateRestrict' is not
    added to the API call parameters.
    """
    # ARRANGE
    mock_get = mocker.patch("requests.Session.get")
    client = GoogleCseClient()

    # ACT
    client.search(query="test", date_filter="invalid_filter")

    # ASSERT
    mock_get.assert_called_once()
    _, call_kwargs = mock_get.call_args
    assert "dateRestrict" not in call_kwargs["params"]


def test_search_api_error_propagates(mocker: MockerFixture, mock_env_vars: None) -> None:
    """
    Verify that an HTTP error from the API call raises a RequestException.
    """
    # ARRANGE
    mock_get = mocker.patch("requests.Session.get")
    mock_get.side_effect = requests.RequestException("API connection failed")
    client = GoogleCseClient()

    # ACT & ASSERT
    with pytest.raises(requests.RequestException, match="API connection failed"):
        client.search(query="test")


def test_search_no_items_found(mocker: MockerFixture, mock_env_vars: None) -> None:
    """
    Verify that the search method returns an empty list when the API
    response contains no 'items' key.
    """
    # ARRANGE
    mock_response = MagicMock()
    mock_response.json.return_value = {"kind": "customsearch#search"}  # No 'items'
    mocker.patch("requests.Session.get", return_value=mock_response)
    client = GoogleCseClient()

    # ACT
    results: list[dict] = client.search(query="test")

    # ASSERT
    assert results == []
