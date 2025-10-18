"""
Unit tests for the job_filters module.

This suite verifies the functionality of the JobFilter class, ensuring that
its scoring, filtering, and sorting logic correctly processes JobPosting
objects based on a set of predefined heuristics.
"""

import pytest

from src.filters.job_filters import JobFilter
from src.models.job_model import JobPosting


@pytest.fixture
def job_filter() -> JobFilter:
    """Provides a reusable instance of the JobFilter class for all tests."""
    return JobFilter()


# Test cases for the private _get_domain method
domain_test_cases = [
    ("https://www.linkedin.com/jobs/search/", "linkedin.com"),
    ("http://jobs.google.com/some/path", "google.com"),
    ("https://gupy.io", "gupy.io"),
    ("https://www.example.co.uk/page", "co.uk"),
    ("not-a-url", ""),
    ("", ""),
]


@pytest.mark.parametrize("link, expected_domain", domain_test_cases)
def test_get_domain(job_filter: JobFilter, link: str, expected_domain: str) -> None:
    """
    Verify that `_get_domain` correctly extracts the parent domain from a URL.
    """
    # ACT
    actual_domain: str = job_filter._get_domain(link=link)
    # ASSERT
    assert actual_domain == expected_domain


def test_calculate_score_high_relevance(job_filter: JobFilter) -> None:
    """
    Verify that a job posting from a good domain with job keywords gets a high score.
    """
    # ARRANGE
    high_relevance_job = JobPosting(
        title="Vaga para Senior Python Developer",
        link="https://www.linkedin.com/jobs/123",
        snippet="We are hiring a new developer for our team.",
        source="linkedin.com",
    )
    # ACT
    score: int = job_filter.calculate_score(job_posting=high_relevance_job)
    # ASSERT
    assert score == 5  # 2 (keywords) + 3 (good domain)


def test_calculate_score_low_relevance(job_filter: JobFilter) -> None:
    """
    Verify that a post from a noise domain with exclusion keywords gets a low score.
    """
    # ARRANGE
    low_relevance_post = JobPosting(
        title="Curso de Python para Desenvolvedores",
        link="https://www.youtube.com/watch?v=abc",
        snippet="This training will teach you Python.",
        source="youtube.com",
    )
    # ACT
    score: int = job_filter.calculate_score(job_posting=low_relevance_post)
    # ASSERT
    assert score == -10  # -5 (noise domain) - 5 (exclusion keyword)


def test_calculate_score_neutral(job_filter: JobFilter) -> None:
    """
    Verify that a post with no strong signals has a score of zero.
    """
    # ARRANGE
    neutral_post = JobPosting(
        title="Python programming language", link="https://www.some-blog.com/article", snippet="An article about Python.", source="some-blog.com"
    )
    # ACT
    score: int = job_filter.calculate_score(job_posting=neutral_post)
    # ASSERT
    assert score == 0


def test_process_filters_and_sorts_correctly(job_filter: JobFilter) -> None:
    """
    Verify that the `process` method correctly filters out low-score items
    and sorts the remaining items by their score in descending order.
    """
    # ARRANGE
    job1_high_score = JobPosting(title="Hiring Python Developer", link="https://gupy.io/1", snippet="", source="gupy.io")  # Score = 5
    job2_medium_score = JobPosting(title="Job: Data Analyst", link="https://neutral.com/2", snippet="", source="neutral.com")  # Score = 2
    job3_noise = JobPosting(title="Curso de Análise de Dados", link="https://youtube.com/3", snippet="", source="youtube.com")  # Score = -5
    job4_no_keywords = JobPosting(title="About our company", link="https://company.com/4", snippet="", source="company.com")  # Score = 0

    results_to_process = [job2_medium_score, job4_no_keywords, job1_high_score, job3_noise]

    # ACT
    processed_list: list[JobPosting] = job_filter.process(results=results_to_process)

    # ASSERT
    # Check that only positive-score items are left
    assert len(processed_list) == 2
    # Check that the list is sorted by score (highest first)
    assert processed_list[0].link == "https://gupy.io/1"  # job1_high_score
    assert processed_list[1].link == "https://neutral.com/2"  # job2_medium_score
    # Check that the scores were attached
    assert processed_list[0].score == 5
    assert processed_list[1].score == 2
