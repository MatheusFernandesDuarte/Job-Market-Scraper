# src/core/builders/query_builder.py


def build_query(location: str | None, seniority: str | None, role: str | None) -> str | None:
    """
    Build a formatted Google search query.

    The query is structured as:
        "{location}" + "{seniority}" + "{role}"

    Example:
        >>> build_query("remote", "Junior", "Data Science")
        '"remote" + "Junior" + "Data Science"'

    Args:
        location (str | None): The job location or work type term (e.g., "remote", "brazil").
        seniority (str | None): The seniority level (e.g., "Junior", "Senior").
        role (str | None): The professional role or field (e.g., "Data Science").

    Returns:
        str | None: A formatted query string if at least one valid term is provided, otherwise None.
    """

    def format_term(term: str | None) -> str | None:
        """
        Clean and enclose a search term in double quotes.

        Args:
            term (str | None): The search term to format.

        Returns:
            str | None: The quoted term, or None if the term is empty or invalid.
        """
        if not term:
            return None
        cleaned: str = term.strip()
        return f'"{cleaned}"' if cleaned else None

    valid_terms: list[str] = [formatted for formatted in map(format_term, [location, seniority, role]) if formatted is not None]

    return " + ".join(valid_terms) if valid_terms else None
