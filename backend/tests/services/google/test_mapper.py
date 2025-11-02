"""
Unit tests for the job_posting_mapper module.

This suite verifies that the mapping function correctly and safely transforms
raw API dictionary data into the structured JobPosting domain model.
"""

from typing import Any

import pytest

from src.models.job_model import JobPosting
from src.services.google.mapper import from_google_cse_item

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def full_google_cse_item() -> dict[str, Any]:
    """Provides a complete, sample 'item' dictionary from the Google CSE API."""
    return {
        "title": "Senior Python Developer",
        "link": "https://example.com/job/123",
        "snippet": "An exciting role for a Python expert on a remote team.",
        "displayLink": "example.com",
        "pagemap": {"metatags": [{"article:published_time": "2025-10-18T10:00:00Z"}]},
    }


@pytest.fixture
def minimal_google_cse_item() -> dict[str, Any]:
    """
    Provides a minimal 'item' dictionary, missing optional fields like
    'pagemap' and 'displayLink'.
    """
    return {
        "title": "Junior Analyst",
        "link": "https://example.com/job/456",
        "snippet": "Entry-level position for a data-driven individual.",
    }


@pytest.fixture
def item_with_empty_pagemap() -> dict[str, Any]:
    """Provides an 'item' with a pagemap that lacks the nested date key."""
    return {
        "title": "Data Engineer",
        "link": "https://example.com/job/789",
        "snippet": "Big data role.",
        "displayLink": "example.com",
        "pagemap": {"metatags": [{}]},
    }


# ==============================================================================
# Test Cases
# ==============================================================================


def test_from_google_cse_item_with_full_data(full_google_cse_item: dict[str, Any]) -> None:
    """
    Verify that a full API item is correctly mapped to a JobPosting object.
    """
    # ACT
    job_posting: JobPosting = from_google_cse_item(item=full_google_cse_item)

    # ASSERT
    assert job_posting.title == "Senior Python Developer"
    assert job_posting.link == "https://example.com/job/123"
    assert job_posting.snippet == "An exciting role for a Python expert on a remote team."
    assert job_posting.source == "example.com"
    assert job_posting.date == "2025-10-18T10:00:00Z"


def test_from_google_cse_item_with_missing_data(minimal_google_cse_item: dict[str, Any]) -> None:
    """
    Verify that a minimal API item is mapped gracefully, with missing fields
    defaulting to empty strings or None.
    """
    # ACT
    job_posting: JobPosting = from_google_cse_item(item=minimal_google_cse_item)

    # ASSERT
    assert job_posting.title == "Junior Analyst"
    assert job_posting.link == "https://example.com/job/456"
    assert job_posting.source == ""  # Should default to empty string
    assert job_posting.date is None  # Should default to None


def test_from_google_cse_item_with_empty_pagemap(item_with_empty_pagemap: dict[str, Any]) -> None:
    """
    Verify that the date is correctly set to None when pagemap or its nested
    keys are missing.
    """
    # ACT
    job_posting: JobPosting = from_google_cse_item(item=item_with_empty_pagemap)

    # ASSERT
    assert job_posting.title == "Data Engineer"
    assert job_posting.date is None


def test_from_google_cse_item_with_empty_dict() -> None:
    """
    Verify that an empty dictionary is handled without errors, resulting in a
    JobPosting with default empty values.
    """
    # ARRANGE
    empty_item: dict[str, Any] = {}

    # ACT
    job_posting: JobPosting = from_google_cse_item(item=empty_item)

    # ASSERT
    assert job_posting.title == ""
    assert job_posting.link == ""
    assert job_posting.snippet == ""
    assert job_posting.source == ""
    assert job_posting.date is None
