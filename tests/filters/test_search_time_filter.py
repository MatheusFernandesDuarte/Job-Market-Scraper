"""
Unit tests for the search_time_filter module.

This suite verifies that the build_time_filter function correctly translates
a number of days into the appropriate Google Search 'tbs' parameter string.
"""

import pytest

from src.filters.search_time_filter import build_time_filter

# A list of test cases covering all logical branches.
# Each tuple contains: (input_days, expected_output_string)
time_filter_test_cases = [
    # Test case for no filter (None input)
    (None, ""),
    # Test case for daily filter (d)
    (1, "qdr:d"),
    # Test case for 0 days (treated as invalid/falsy by the function)
    (0, ""),
    # Test case for negative days (falls into the <= 1 condition)
    (-1, "qdr:d"),
    # Test case for weekly filter (w)
    (7, "qdr:w"),
    # Test a value within the weekly range
    (3, "qdr:w"),
    # Test case for monthly filter (m)
    (30, "qdr:m"),
    # Test a value within the monthly range
    (15, "qdr:m"),
    # Test case for a value greater than the max range
    (31, ""),
    # Test a large value
    (100, ""),
]


@pytest.mark.parametrize("days_input, expected_result", time_filter_test_cases)
def test_build_time_filter(days_input: int | None, expected_result: str) -> None:
    """
    Verify `build_time_filter` returns the correct string for various day inputs.

    This parameterized test covers the following scenarios:
    - No input (None).
    - Values corresponding to daily, weekly, and monthly filters.
    - Edge cases at the boundaries of each range (e.g., 1, 7, 30).
    - Values outside the maximum supported range.

    Args:
        days_input (int | None): The number of days to pass to the function.
        expected_result (str): The expected 'tbs' parameter string.

    Returns:
        None
    """
    # ACT: Call the function with the test case input
    actual_result: str = build_time_filter(days=days_input)

    # ASSERT: Check if the actual output matches the expected output
    assert actual_result == expected_result
