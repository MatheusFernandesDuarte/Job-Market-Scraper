# backend/src/core/builders/query_builder.py

from typing import Iterable


def build_query(location: str | None, seniority: str | None, role: str | None) -> str | None:
    """
    Build a formatted Google search query.

    The query is structured as:
        "{location}" + "{seniority}" + "{role}"

    Args:
        location (str | None): The job location or work type term (e.g., "remote", "brazil").
        seniority (str | None): The seniority level (e.g., "Junior", "Senior").
        role (str | None): The professional role or field (e.g., "Data Science").

    Returns:
        str | None: A formatted query string if at least one valid term is provided, otherwise None.
    """

    def sanitize_term(term: str | None) -> str | None:
        """
        Sanitize a search term.

        Args:
            term (str | None): The search term to format.

        Returns:
            str | None: The sanitized term, or None if the term is empty or invalid.
        """
        if not term:
            return None
        if isinstance(term, Iterable) and not isinstance(term, str):
            raise ValueError(f"Expected string, got iterable: {term}")
        cleaned: str = term.strip().strip("[]\"'")
        return f'"{cleaned}"' if cleaned else None

    valid_terms: list[str] = [t for t in map(sanitize_term, [location, seniority, role]) if t is not None]

    return " + ".join(valid_terms) if valid_terms else None

