# src/services/base.py

from abc import ABC, abstractmethod

from src.models.job_model import JobPosting


class BaseProvider(ABC):
    """Abstract base class for any job search provider."""

    @abstractmethod
    def search(self, queries: list[str], max_results: int = 10) -> list[JobPosting]:
        """
        Perform a search using the provider.

        Args:
            queries (list[str]): A list of search query strings to execute.
            max_results (int): The maximum number of unique results to return.

        Returns:
            list[JobPosting]: A list of deduplicated and filtered JobPosting
            instances.
        """
        raise NotImplementedError
