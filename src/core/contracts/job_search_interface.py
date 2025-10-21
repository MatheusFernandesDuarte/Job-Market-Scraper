# src/core/contracts/job_search_interface.py
from abc import ABC, abstractmethod

from src.models.job_model import JobPosting


class JobSearchInterface(ABC):
    """
    Abstract interface for any job search service.

    This contract ensures that any service implementation (e.g., Google,
    LinkedIn, etc.) will have a consistent `search` method, allowing them
    to be used interchangeably by the application's core logic.
    """

    @abstractmethod
    def search(self, queries: list[str], max_results: int = 10) -> list[JobPosting]:
        """
        Perform a search using the service.

        Args:
            queries (list[str]): A list of search query strings to execute.
            max_results (int): The maximum number of unique results to return.

        Returns:
            list[JobPosting]: A list of deduplicated and filtered JobPosting
                              instances.
        """
        raise NotImplementedError
