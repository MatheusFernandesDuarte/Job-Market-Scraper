"""
Unit tests for the query_builder module.

This test suite verifies the functionality of the build_query function,
ensuring it correctly formats and combines search terms under various
conditions, including handling of empty, None, and whitespace-padded inputs.
"""

import pytest

from backend.src.core.builders.query_builder import build_query

# A list of test cases covering various scenarios
# Each tuple contains: (location, seniority, role, expected_output)
query_test_cases = [
    # Happy path: all terms provided
    ("remote", "senior", "python developer", '"remote" + "senior" + "python developer"'),
    # One term missing (None)
    ("brazil", "junior", None, '"brazil" + "junior"'),
    # One term missing (empty string)
    ("latam", "", "data analyst", '"latam" + "data analyst"'),
    # Two terms missing
    (None, None, "RPA", '"RPA"'),
    ("remote", None, "", '"remote"'),
    # All terms missing
    (None, None, None, None),
    ("", "", "", None),
    ("   ", "", None, None),
    # Terms with leading/trailing whitespace
    ("  remote  ", "junior", " data science ", '"remote" + "junior" + "data science"'),
    # Terms that are only whitespace
    ("   ", "pleno", "backend", '"pleno" + "backend"'),
]


@pytest.mark.parametrize("location, seniority, role, expected", query_test_cases)
def test_build_query(location: str | None, seniority: str | None, role: str | None, expected: str | None) -> None:
    """
    Test the build_query function with various combinations of inputs.

    This parameterized test covers the following scenarios:
    - All terms are valid strings.
    - Some terms are None or empty strings.
    - All terms are invalid (None or empty).
    - Terms contain extra whitespace that should be stripped.

    Args:
        location (str | None): The location term for the test case.
        seniority (str | None): The seniority term for the test case.
        role (str | None): The role term for the test case.
        expected (str | None): The expected formatted query string, or None.

    Returns:
        None
    """
    # ACT: Call the function with the test case inputs
    actual_query: str | None = build_query(location=location, seniority=seniority, role=role)

    # ASSERT: Check if the actual output matches the expected output
    assert actual_query == expected


def test_build_query_returns_none_for_all_whitespace_terms() -> None:
    """
    Verify that build_query returns None if all terms consist only of whitespace.

    This is a specific edge case to ensure that strings containing only spaces
    are correctly identified as invalid.
    """
    # ARRANGE
    location: str = "   "
    seniority: str = "\t"
    role: str = "\n"

    # ACT
    result: str | None = build_query(location, seniority, role)

    # ASSERT
    assert result is None

