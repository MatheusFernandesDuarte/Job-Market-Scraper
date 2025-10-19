# src/filters/query_expander.py

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
        Expand each query with its synonyms.

        Args:
            queries (Iterable[str]): Base queries.

        Returns:
            list[str]: Expanded queries including originals + synonyms.
        """
        expanded: set[str] = set()

        for q in queries:
            q_lower: str = q.lower().strip()
            expanded.add(q_lower)

            for keyword, synonyms in self._SYNONYMS.items():
                pattern: str = rf'(?<!\w)"?{re.escape(pattern=keyword)}"?(?!\w)'
                if re.search(pattern=pattern, string=q_lower):
                    for s in synonyms:
                        expanded.add(q_lower.replace(keyword, s))
                    expanded.update(synonyms)

        return list(expanded)
