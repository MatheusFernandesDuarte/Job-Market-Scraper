# src/core/filters/query_expander.py

import re
from typing import Iterable


class QueryExpander:
    """
    Expand search queries with predefined synonyms and variations.
    Useful for covering broader terminology in job searches.
    """

    _SYNONYMS: dict[str, list[str]] = {
        "dev": ["developer", "engineer", "programmer"],
        "developer": ["engineer", "programmer"],
        "frontend": ["front-end", "ui developer", "react", "vue", "angular"],
        "backend": ["back-end", "api developer", "django", "node.js"],
        "fullstack": ["full-stack", "frontend backend"],
        "data": ["data analyst", "data scientist", "machine learning"],
    }

    def expand(self, queries: Iterable[str]) -> list[str]:
        """
        Expands each query by substituting keywords with their synonyms.

        Args:
            queries (Iterable[str]): Base queries.

        Returns:
            list[str]: Expanded queries including originals + synonyms.
        """
        expanded: set[str] = set()

        for q in queries:
            q_lower: str = q.lower().strip()
            expanded.add(q_lower)
            words_in_query: set[str] = set(re.findall(pattern=r"\b\w+\b", string=q_lower))

            for keyword, synonyms in self._SYNONYMS.items():
                if keyword in words_in_query:
                    for s in synonyms:
                        new_query: str = q_lower.replace(keyword, s)
                        expanded.add(new_query)

        return list(expanded)
