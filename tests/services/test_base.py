"""
Unit tests for the BaseProvider abstract base class.

This suite verifies the contract of the BaseProvider, ensuring that it cannot
be instantiated directly and that subclasses must implement the abstract
`search` method.
"""

import pytest

from src.models.job_model import JobPosting
from src.services.base import BaseProvider


def test_cannot_instantiate_base_provider_directly() -> None:
    """
    Verify that instantiating the abstract BaseProvider directly raises a TypeError.
    """
    # ARRANGE & ACT & ASSERT
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        BaseProvider()  # type: ignore


def test_concrete_provider_can_be_instantiated() -> None:
    """
    Verify that a concrete class that inherits from BaseProvider and implements
    all abstract methods can be instantiated without error.
    """

    # ARRANGE
    class ConcreteProvider(BaseProvider):
        """A valid, minimal implementation of the BaseProvider."""

        def search(self, queries: list[str], max_results: int = 10) -> list[JobPosting]:
            return []

    # ACT & ASSERT
    try:
        provider = ConcreteProvider()
        assert isinstance(provider, BaseProvider)
    except TypeError:
        pytest.fail("Instantiation of a valid concrete provider should not raise a TypeError.")


def test_incomplete_provider_raises_type_error() -> None:
    """
    Verify that a class inheriting from BaseProvider without implementing the
    `search` method raises a TypeError upon instantiation.
    """

    # ARRANGE
    class IncompleteProvider(BaseProvider):
        """An invalid implementation that is missing the 'search' method."""

        pass

    # ACT & ASSERT
    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteProvider"):
        IncompleteProvider()  # type: ignore
