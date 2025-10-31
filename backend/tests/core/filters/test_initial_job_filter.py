# backend/tests/core/filters/test_initial_job_filter.py

import pytest
import tldextract

from backend.src.core.filters.initial_job_filter import InitialJobFilter
from backend.src.models.job_model import JobPosting


@pytest.mark.parametrize(
    "link, expected_domain",
    [
        ("https://www.linkedin.com/jobs/search/", "linkedin.com"),
        ("http://jobs.google.com/some/path", "google.com"),
        ("https://www.example.co.uk/page", "example.co.uk"),
        ("invalid-url", "invalid-url"),  # corrected expectation
        ("", ""),  # still empty
    ],
)
def test_get_domain_extracts_correctly(link: str, expected_domain: str) -> None:
    """Ensure _get_domain extracts parent domain safely and correctly."""
    result = InitialJobFilter._get_domain(link)
    assert result == expected_domain


def test_get_domain_handles_exception(monkeypatch):
    """Ensure _get_domain returns empty string on internal parsing error."""

    def mock_extract(_):
        raise ValueError("mocked failure")

    monkeypatch.setattr(tldextract, "extract", mock_extract)
    assert InitialJobFilter._get_domain("http://test.com") == ""


@pytest.mark.parametrize(
    "job, expected",
    [
        (
            JobPosting(
                title="Python Developer",
                link="https://jobs.lever.co/123",
                snippet="We are hiring backend engineers",
                source="lever.co",
            ),
            True,
        ),
        (
            JobPosting(
                title="Python Developer",
                link="https://www.youtube.com/watch?v=123",
                snippet="Learn Python basics",
                source="youtube.com",
            ),
            False,
        ),
        (
            JobPosting(
                title="Analista de Recursos Humanos",
                link="https://company.com/job",
                snippet="vaga administrativa",
                source="company.com",
            ),
            False,
        ),
        (
            JobPosting(
                title="Python Developer Tutorial",
                link="https://company.com/blog",
                snippet="Learn to build web apps",
                source="company.com",
            ),
            False,
        ),
        (
            JobPosting(
                title="Software Engineer",
                link="",
                snippet="Work remotely",
                source="unknown",
            ),
            False,
        ),
    ],
)
def test_should_keep_filters_correctly(job: JobPosting, expected: bool) -> None:
    """Ensure should_keep correctly filters jobs by domain, title, and snippet."""
    assert InitialJobFilter.should_keep(job) == expected
