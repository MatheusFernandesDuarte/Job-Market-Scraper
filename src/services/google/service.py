# src/services/google/service.py

import requests

from src.filters.job_filters import JobFilter
from src.filters.search_time_filter import build_time_filter
from src.models.job_model import JobPosting
from src.services.base import BaseProvider
from src.services.google.client import GoogleCseClient
from src.services.google.mapper import from_google_cse_item


class GoogleService(BaseProvider):
    """
    Service responsible for fetching, processing, and filtering job postings
    from Google Custom Search Engine (CSE).

    This service:
        - Builds and executes queries using GoogleCseClient
        - Maps raw API responses into JobPosting domain models
        - Filters, deduplicates, and adjusts search range adaptively
    """

    _SEARCH_WINDOWS: list[int | None] = [7, 14, 30, 90, 180, None]

    def __init__(self, client: GoogleCseClient | None = None) -> None:
        """
        Initialize the GoogleService.

        Args:
            client (GoogleCseClient | None): Custom CSE client instance.
                If None, a default one is created.
        """
        self.client: GoogleCseClient = client or GoogleCseClient()
        self.filter: JobFilter = JobFilter()

    def search(self, queries: list[str], max_results: int = 10) -> list[JobPosting]:
        """
        Perform adaptive searches for job postings from Google CSE.

        It starts filtering results by the last 7 days and progressively expands
        the time range (14, 30, 90, 180, then no limit) until at least
        `max_results` unique job postings are found or all ranges are exhausted.

        Args:
            queries (list[str]): Search query strings.
            max_results (int): Desired number of unique job postings.

        Returns:
            list[JobPosting]: A list of up to `max_results` job postings,
            filtered and deduplicated.
        """
        all_candidates: dict[str, JobPosting] = {}

        for window in self._SEARCH_WINDOWS:
            date_filter: str = build_time_filter(days=window)
            window_label: str = f"{window} days" if window else "no time filter"
            print(f"🔎 Searching jobs ({window_label})...")

            for query in queries:
                try:
                    raw_items: list[dict] = self.client.search(query=query, date_filter=date_filter)

                    for item in raw_items:
                        job_posting: JobPosting = from_google_cse_item(item=item)
                        if job_posting.link and job_posting.link not in all_candidates:
                            all_candidates[job_posting.link] = job_posting

                except requests.RequestException:
                    continue

            filtered_results: list[JobPosting] = self.filter.process(results=list(all_candidates.values()))

            if len(filtered_results) >= max_results:
                break

        return filtered_results[:max_results]
