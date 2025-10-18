"""
Unit tests for the CLI UI module.

This suite uses the 'capsys' fixture to capture standard output and verify
that each display function prints the correct, styled information to the
console.
"""

import pytest
from _pytest.capture import CaptureFixture

from src.interface.cli import ui
from src.models.job_model import JobPosting

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def sample_job_postings() -> list[JobPosting]:
    """Provides a list of sample JobPosting objects for testing display."""
    return [
        JobPosting(
            title="Senior Python Developer",
            link="https://example.com/job/1",
            snippet="First exciting job opportunity.",
            source="example.com",
            date="2025-10-18T10:00:00Z",
        ),
        JobPosting(
            title="Junior Data Analyst",
            link="https://example.com/job/2",
            snippet="Second role for data enthusiasts.",
            source="another.com",
            date=None,
        ),
    ]


# ==============================================================================
# Test Cases
# ==============================================================================


def test_display_search_header(capsys: CaptureFixture) -> None:
    """
    Verify that the search header and all provided queries are printed.

    Args:
        capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
    """
    # ARRANGE
    queries: list[str] = ['"remote" + "python"', '"data science"']

    # ACT
    ui.display_search_header(queries=queries)
    captured_output: str = capsys.readouterr().out

    # ASSERT
    assert "Running searches for:" in captured_output
    assert '"remote" + "python"' in captured_output
    assert '"data science"' in captured_output


def test_display_results_with_jobs(capsys: CaptureFixture, sample_job_postings: list[JobPosting]) -> None:
    """
    Verify that a list of job postings is formatted and printed correctly.

    Args:
        capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
        sample_job_postings (list[JobPosting]): A fixture providing sample jobs.
    """
    # ARRANGE
    results: list[JobPosting] = sample_job_postings

    # ACT
    ui.display_results(results=results)
    captured_output: str = capsys.readouterr().out

    # ASSERT
    assert "Top job postings:" in captured_output
    assert "Senior Python Developer" in captured_output
    assert "Source:" in captured_output
    assert "example.com" in captured_output
    assert "Link:" in captured_output
    assert "https://example.com/job/1" in captured_output
    assert "Snippet:" in captured_output
    assert "First exciting job opportunity." in captured_output
    assert "Junior Data Analyst" in captured_output
    assert "another.com" in captured_output


def test_display_results_with_no_jobs(capsys: CaptureFixture) -> None:
    """
    Verify that the 'No results found' message is printed for an empty list.

    Args:
        capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
    """
    # ARRANGE
    results: list[JobPosting] = []

    # ACT
    ui.display_results(results=results)
    captured_output: str = capsys.readouterr().out

    # ASSERT
    assert "No results found." in captured_output
    assert "Top job postings:" not in captured_output


def test_display_error(capsys: CaptureFixture) -> None:
    """
    Verify that an error message is printed in the correct format.

    Args:
        capsys (CaptureFixture): Pytest fixture to capture stdout and stderr.
    """
    # ARRANGE
    error_message: str = "API key is invalid."

    # ACT
    ui.display_error(message=error_message)
    captured_output: str = capsys.readouterr().out

    # ASSERT
    assert "[error]" in captured_output
    assert "API key is invalid." in captured_output
