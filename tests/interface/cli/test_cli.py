"""
Unit tests for the main CLI orchestrator module.

This suite uses extensive mocking to isolate the `main` function from its
dependencies (argument parsing, UI, services) and verify its core
orchestration logic under various conditions.
"""

from argparse import Namespace
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.interface.cli import cli
from src.models.job_model import JobPosting

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def mock_args_parser(mocker: MockerFixture) -> MagicMock:
    """Mocks the cli_args.parse_args function."""
    return mocker.patch("src.interface.cli.cli.cli_args.parse_args")


@pytest.fixture
def mock_ui(mocker: MockerFixture) -> MagicMock:
    """Mocks the entire cli_ui module."""
    return mocker.patch("src.interface.cli.cli.cli_ui", autospec=True)


@pytest.fixture
def mock_service(mocker: MockerFixture) -> MagicMock:
    """Mocks the create_service factory and the returned service instance."""
    mock_service_instance = mocker.MagicMock()
    mocker.patch("src.interface.cli.cli.create_service", return_value=mock_service_instance)
    return mock_service_instance


# ==============================================================================
# Test Cases
# ==============================================================================


def test_main_successful_flow(mock_args_parser: MagicMock, mock_ui: MagicMock, mock_service: MagicMock) -> None:
    """
    Verify the entire successful execution path from args to results.
    """
    # ARRANGE
    args = Namespace(locations=["remote"], seniority=["senior"], role=["Python"], max=5)
    mock_args_parser.return_value = args

    sample_results = [JobPosting("Test Job", "link", "snippet", "source")]
    mock_service.search.return_value = sample_results

    # ACT
    exit_code: int = cli.main(argv=[])

    # ASSERT
    assert exit_code == 0
    mock_args_parser.assert_called_once()
    mock_ui.display_search_header.assert_called_once_with(queries=['"remote" + "senior" + "Python"'])
    mock_service.search.assert_called_once_with(queries=['"remote" + "senior" + "Python"'], max_results=5)
    mock_ui.display_results.assert_called_once_with(results=sample_results)
    mock_ui.display_error.assert_not_called()


def test_main_returns_error_if_no_criteria_provided(mock_args_parser: MagicMock, mock_ui: MagicMock) -> None:
    """
    Verify that an error is shown and the program exits if no search args are given.
    """
    # ARRANGE
    args = Namespace(locations=[""], seniority=[""], role=[""])
    mock_args_parser.return_value = args

    # ACT
    exit_code: int = cli.main(argv=[])

    # ASSERT
    assert exit_code == 1
    mock_ui.display_error.assert_called_once_with("Please provide at least one search criterion (--locations, --seniority, or --role).")


def test_main_returns_error_if_no_valid_queries_built(mock_args_parser: MagicMock, mock_ui: MagicMock) -> None:
    """
    Verify that an error is shown if the provided terms result in no valid queries.
    """
    # ARRANGE
    args = Namespace(locations=[" "], seniority=[""], role=[""])  # Will result in empty query
    mock_args_parser.return_value = args

    # ACT
    exit_code: int = cli.main(argv=[])

    # ASSERT
    assert exit_code == 1
    mock_ui.display_error.assert_called_once_with(message="Could not build any valid queries from the provided terms.")


def test_main_handles_service_creation_exception(mocker: MockerFixture, mock_args_parser: MagicMock, mock_ui: MagicMock) -> None:
    """
    Verify that an exception during service creation is caught and handled.
    """
    # ARRANGE
    args = Namespace(locations=["remote"], seniority=[""], role=["Python"], max=10)
    mock_args_parser.return_value = args

    error_message = "API keys not found"
    mocker.patch("src.interface.cli.cli.create_service", side_effect=RuntimeError(error_message))

    # ACT
    exit_code: int = cli.main(argv=[])

    # ASSERT
    assert exit_code == 2
    mock_ui.display_error.assert_called_once_with(message=f"An error occurred during the search: {error_message}")


def test_main_handles_search_exception(mock_args_parser: MagicMock, mock_ui: MagicMock, mock_service: MagicMock) -> None:
    """
    Verify that an exception during the search call is caught and handled.
    """
    # ARRANGE
    args = Namespace(locations=["remote"], seniority=[""], role=["Python"], max=10)
    mock_args_parser.return_value = args

    error_message = "Network timeout"
    mock_service.search.side_effect = Exception(error_message)

    # ACT
    exit_code: int = cli.main(argv=[])

    # ASSERT
    assert exit_code == 2
    mock_ui.display_error.assert_called_once_with(message=f"An error occurred during the search: {error_message}")
