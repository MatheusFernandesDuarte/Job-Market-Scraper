# src/filters/search_time_filter.py


def build_time_filter(days: int | None = None) -> str:
    """
    Build a Google Search time filter parameter.

    Args:
        days (Optional[int]): Number of days to filter (1, 7, 30).

    Returns:
        str: The 'tbs' parameter value (e.g., 'qdr:d', 'qdr:w', 'qdr:m'), or an empty string.
    """
    if not days:
        return ""
    if days <= 1:
        return "qdr:d"
    if days <= 7:
        return "qdr:w"
    if days <= 30:
        return "qdr:m"
    return ""
