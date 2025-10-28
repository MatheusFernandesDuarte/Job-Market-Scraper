# backend/tests/interface/cli/test_ui.py
from unittest.mock import MagicMock

import pytest

from backend.src.interface.cli import ui
from backend.src.models.job_model import JobPosting


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
    mocker.patch("backend.src.interface.cli.ui.Styler", MockStyler)


def test_display_results_with_jobs() -> None:
    """
    Tests if results are formatted correctly.
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
    result_str = ui.display_results(results=jobs)

    # Assert
    assert "Software Engineer" in result_str
    assert "http://job.com/1" in result_str
    assert "This is a full description." in result_str


def test_display_results_empty() -> None:
    """
    Tests the output when no results are found.
    """
    # Act
    result_str = ui.display_results(results=[])

    # Assert
    assert "No results found" in result_str


def test_display_error() -> None:
    """
    Tests if error messages are formatted correctly.
    """
    # Act
    error_str = ui.display_error(message="Test error")

    # Assert
    assert "[ERROR][error] Test error[/ERROR]" in error_str

