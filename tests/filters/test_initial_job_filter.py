# tests/core/filters/test_initial_job_filter.py

import pytest

from src.core.filters.initial_job_filter import InitialJobFilter
from src.models.job_model import JobPosting

domain_test_cases = [
    ("https://www.linkedin.com/jobs/search/", "linkedin.com"),
    ("http://jobs.google.com/some/path", "google.com"),
    ("https://www.example.co.uk/page", "co.uk"),
    ("not-a-url", ""),
]


@pytest.mark.parametrize("link, expected_domain", domain_test_cases)
def test_get_domain(link: str, expected_domain: str) -> None:
    """
    Tests if the private method _get_domain correctly extracts the parent domain.
    """
    assert InitialJobFilter._get_domain(link=link) == expected_domain


should_keep_test_cases = [
    (JobPosting(title="Python Developer", link="https://jobs.lever.co/1", snippet="Hiring for a new role", source="lever.co"), True),
    (JobPosting(title="Senior Developer", link="https://www.youtube.com/1", snippet="A video", source="youtube.com"), False),
    (JobPosting(title="All our open jobs", link="https://company.com/1", snippet="See our openings", source="company.com"), False),
    (JobPosting(title="Developer position", link="https://company.com/1", snippet="Check our average salary...", source="company.com"), False),
]


@pytest.mark.parametrize("job_posting, should_be_kept", should_keep_test_cases)
def test_should_keep(job_posting: JobPosting, should_be_kept: bool) -> None:
    """
    Tests the main filtering logic of the should_keep method.
    """
    assert InitialJobFilter.should_keep(job=job_posting) == should_be_kept
