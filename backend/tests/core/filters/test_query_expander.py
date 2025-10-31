# backend/tests/core/filters/test_query_expander.py

import pytest

from backend.src.core.filters.query_expander import QueryExpander

test_cases = [
    (['"python developer"'], {'"python developer"', '"python engineer"', '"python programmer"'}),
    (['"brazil" + "python developer"'], {'"brazil" + "python developer"', '"brazil" + "python engineer"', '"brazil" + "python programmer"'}),
    (['"devops role"'], {'"devops role"'}),
    (
        ['"backend"', '"data"'],
        {'"backend"', '"back-end"', '"api developer"', '"django"', '"node.js"', '"data"', '"data analyst"', '"data scientist"', '"machine learning"'},
    ),
    (
        ['"react"'],
        {'"react"'},
    ),
]


@pytest.mark.parametrize("input_queries, expected_expansion", test_cases)
def test_query_expander(input_queries: list[str], expected_expansion: set[str]) -> None:
    """
    Tests that the QueryExpander correctly expands queries by substitution
    and handles various cases.
    """
    # Arrange
    expander = QueryExpander()

    # Act
    actual_expansion = expander.expand(queries=input_queries)

    # Assert
    assert set(actual_expansion) == expected_expansion
