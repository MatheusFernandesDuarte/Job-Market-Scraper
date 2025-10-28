# backend/src/core/filters/search_time_filter.py

from __future__ import annotations


def build_time_filter(days: int | None) -> str | None:
    """
    Builds a dateRestrict string compatible with the Google CSE API.

    The format is [d,w,m,y]NUMBER, specifying a search within the last
    N days, weeks, months, or years.

    Args:
        days (int | None): The number of days for the time window.

    Returns:
        str | None: A formatted string for the dateRestrict parameter,
                    or None if no filter should be applied.
    """
    if days is None:
        return None

    if days <= 7:
        return "w1"  # last week
    if days <= 14:
        return "w2"  # last 2 weeks
    if days <= 30:
        return "m1"  # last month
    if days <= 90:
        return "m3"  # last 3 months
    if days <= 180:
        return "m6"  # last 6 months

    return None

