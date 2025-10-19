# test_query_expander.py

from src.filters.query_expander import QueryExpander

expander: QueryExpander = QueryExpander()

queries: list[str] = ['"brazil" + "developer"']
expanded: list[str] = expander.expand(queries=queries)
expected_result: list[str] = ["engineer", '"brazil" + "programmer"', '"brazil" + "developer"', "programmer", '"brazil" + "engineer"']

assert set(expanded) == set(expected_result)
