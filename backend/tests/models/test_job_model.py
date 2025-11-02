"""
Unit tests for the job_model module.

This suite verifies that the JobPosting dataclass correctly initializes
with both required and optional attributes, and that its default values
are set as expected.
"""

from src.models.job_model import JobPosting


def test_job_posting_instantiation_with_all_fields() -> None:
    """
    Verify that a JobPosting object is created correctly with all fields provided.
    """
    # ARRANGE
    title = "Senior Python Developer"
    link = "https://example.com/job/123"
    snippet = "An exciting role for a Python expert."
    source = "example.com"
    date = "2025-10-18T10:00:00Z"

    # ACT
    job_posting = JobPosting(title=title, link=link, snippet=snippet, source=source, date=date)

    # ASSERT
    assert job_posting.title == title
    assert job_posting.link == link
    assert job_posting.snippet == snippet
    assert job_posting.source == source
    assert job_posting.date == date


def test_job_posting_instantiation_with_optional_fields_missing() -> None:
    """
    Verify that a JobPosting object is created correctly when optional fields
    like 'date' are not provided.
    """
    # ARRANGE & ACT
    job_posting = JobPosting(
        title="Junior Analyst",
        link="https://example.com/job/456",
        snippet="Entry-level position.",
        source="example.com",
    )

    # ASSERT
    assert job_posting.title == "Junior Analyst"
    assert job_posting.date is None


def test_job_posting_score_defaults_to_zero() -> None:
    """
    Verify that the 'score' attribute defaults to 0 upon instantiation.
    """
    # ARRANGE & ACT
    job_posting = JobPosting(
        title="Data Engineer",
        link="https://example.com/job/789",
        snippet="Big data role.",
        source="example.com",
    )

    # ASSERT
    assert job_posting.score == 0


def test_job_posting_score_is_not_in_repr() -> None:
    """
    Verify that the 'score' attribute is not included in the object's
    string representation, as specified by repr=False.
    """
    # ARRANGE
    job_posting = JobPosting(
        title="Manager",
        link="https://example.com/job/101",
        snippet="Leadership role.",
        source="example.com",
    )
    job_posting.score = 10  # Assign a score to test its representation

    # ACT
    representation: str = repr(job_posting)

    # ASSERT
    assert "score=10" not in representation
    assert "title='Manager'" in representation  # Confirm other fields are present
