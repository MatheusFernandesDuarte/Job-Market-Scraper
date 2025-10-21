# tests/interface/cli/test_ui.py
from unittest.mock import MagicMock

import pytest

from src.interface.cli import ui
from src.models.job_model import JobPosting


# Mock a Styler class so we don't need the actual styling library for tests
class MockStyler:
    @staticmethod
    def title(text: str) -> str:
        return f"[TITLE]{text}[/TITLE]"

    @staticmethod
    def info(text: str) -> str:
        return f"[INFO]{text}[/INFO]"

    @staticmethod
    def success(text: str) -> str:
        return f"[SUCCESS]{text}[/SUCCESS]"

    @staticmethod
    def warning(text: str) -> str:
        return f"[WARNING]{text}[/WARNING]"

    @staticmethod
    def error(text: str) -> str:
        return f"[ERROR]{text}[/ERROR]"

    @staticmethod
    def dim(text: str) -> str:
        return f"[DIM]{text}[/DIM]"


@pytest.fixture(autouse=True)
def mock_styler(mocker: MagicMock) -> None:
    """Automatically replaces the Styler with a mock for all tests in this file."""
    mocker.patch("src.interface.cli.ui.Styler", MockStyler)


def test_display_results_with_jobs(capsys) -> None:
    """
    Tests if results are printed correctly.
    """
    # Arrange
    jobs = [
        JobPosting(
            title="Software Engineer",
            link="http://job.com/1",
            source="Test Source",
            snippet="snippet",
            full_description="This is a full description.",
        )
    ]

    # Act
    ui.display_results(results=jobs)
    captured = capsys.readouterr()

    # Assert
    assert "Software Engineer" in captured.out
    assert "http://job.com/1" in captured.out
    assert "This is a full description." in captured.out


def test_display_results_empty(capsys) -> None:
    """
    Tests the output when no results are found.
    """
    # Arrange
    ui.display_results(results=[])
    captured = capsys.readouterr()

    # Assert
    assert "No results found" in captured.out


def test_display_error(capsys) -> None:
    """
    Tests if error messages are displayed correctly.
    """
    # Arrange
    ui.display_error(message="Test error")
    captured = capsys.readouterr()

    # Assert
    assert "[ERROR][error] Test error[/ERROR]" in captured.out
