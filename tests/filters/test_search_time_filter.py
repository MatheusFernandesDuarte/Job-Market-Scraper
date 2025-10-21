# tests/filters/test_search_time_filter.py

"""
Unit tests for the search_time_filter module.

This suite verifies that the build_time_filter function correctly translates
a number of days into the appropriate Google Custom Search 'dateRestrict' parameter.
"""

import pytest

from src.core.filters.search_time_filter import build_time_filter

# Each tuple: (input_days, expected_output)
time_filter_test_cases = [
    # No filter
    (None, None),
    # Up to 7 days -> last week
    (1, "w1"),
    (7, "w1"),
    # Between 8–14 days -> last 2 weeks
    (8, "w2"),
    (14, "w2"),
    # Between 15–30 days -> last month
    (15, "m1"),
    (30, "m1"),
    # Between 31–90 days -> last 3 months
    (31, "m3"),
    (90, "m3"),
    # Between 91–180 days -> last 6 months
    (91, "m6"),
    (180, "m6"),
    # Beyond 180 days -> no filter
    (181, None),
    (365, None),
    # Negative or zero days -> still treated as recent (<=7)
    (0, "w1"),
    (-5, "w1"),
]


@pytest.mark.parametrize("days_input, expected_result", time_filter_test_cases)
def test_build_time_filter(days_input: int | None, expected_result: str | None) -> None:
    """
    Ensure `build_time_filter` returns the correct 'dateRestrict' value
    for a variety of day-based inputs.

    This includes:
      - None input (no filter)
      - Weekly, biweekly, monthly, and multi-month filters
      - Edge cases at each boundary
      - Values outside valid ranges (return None)
    """
    # ACT
    result = build_time_filter(days_input)

    # ASSERT
    assert result == expected_result, f"For days={days_input}, expected {expected_result!r} but got {result!r}"
