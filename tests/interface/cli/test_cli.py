# tests/interface/cli/test_cli.py

from unittest.mock import ANY, AsyncMock, MagicMock

import pytest

from src.interface.cli import cli

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_use_case(mocker: MagicMock) -> MagicMock:
    """Mocks the JobSearchAndEnrichUseCase using a stable, absolute path."""
    mock = mocker.patch("src.interface.cli.cli.JobSearchAndEnrichUseCase")
    mock.return_value.execute = AsyncMock(return_value=["job1"])
    return mock


@pytest.fixture
def mock_ui(mocker: MagicMock) -> MagicMock:
    """Mocks the UI module and configures return values for its functions."""
    mock = mocker.patch("src.interface.cli.cli.cli_ui")
    mock.display_results.return_value = "---Fake Results---"
    mock.display_error.return_value = "---Fake Error---"
    mock.display_search_header.return_value = "---Fake Header---"
    return mock


@pytest.fixture
def mock_scraper(mocker: MagicMock) -> MagicMock:
    """Mocks the PlaywrightScraper to prevent a real browser launch."""
    return mocker.patch("src.interface.cli.cli.PlaywrightScraper")


@pytest.fixture
def mock_logger_info(mocker: MagicMock) -> MagicMock:
    """Mocks the 'info' method of the logger in the cli module."""
    return mocker.patch("src.interface.cli.cli.logger.info")


async def test_main_success_flow(
    mock_use_case: MagicMock,
    mock_ui: MagicMock,
    mock_scraper: MagicMock,
    mock_logger_info: MagicMock,
) -> None:
    """Tests the successful execution path of the CLI."""
    argv = ["--role", "Developer", "--max", "5"]

    exit_code = await cli.main(argv=argv)

    mock_use_case.assert_called_once()
    mock_use_case.return_value.execute.assert_awaited_once_with(queries=['"Developer"'], max_results=5)

    mock_ui.display_results.assert_called_once_with(results=["job1"])
    mock_logger_info.assert_any_call("---Fake Results---")

    assert exit_code == 0


async def test_main_no_args_error(mock_use_case: MagicMock, mock_ui: MagicMock) -> None:
    argv = []
    exit_code = await cli.main(argv=argv)
    mock_ui.display_error.assert_called_once()
    assert exit_code == 1
    mock_use_case.return_value.execute.assert_not_awaited()


async def test_main_handles_exception(mock_use_case: MagicMock, mock_ui: MagicMock) -> None:
    mock_use_case.return_value.execute.side_effect = Exception("Something went wrong")
    argv = ["--role", "Engineer"]

    exit_code = await cli.main(argv=argv)

    mock_ui.display_error.assert_called_once_with(message=ANY)
    assert exit_code == 2
