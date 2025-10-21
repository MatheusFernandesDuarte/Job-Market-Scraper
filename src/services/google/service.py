# src/services/google/service.py

import logging

import requests

from src.core.contracts.job_search_interface import JobSearchInterface
from src.core.filters.initial_job_filter import InitialJobFilter
from src.core.filters.query_expander import QueryExpander
from src.core.filters.search_time_filter import build_time_filter
from src.models.job_model import JobPosting
from src.services.google.client import GoogleCseClient
from src.services.google.mapper import from_google_cse_item

logger = logging.getLogger(__name__)


class GoogleService(JobSearchInterface):
    """
    Service responsible for fetching, processing, and filtering job postings
    from Google Custom Search Engine (CSE).
    """

    _SEARCH_WINDOWS: list[int | None] = [7, 14, 30, 90, 180, None]

    def __init__(self, client: GoogleCseClient | None = None, expander: QueryExpander | None = None) -> None:
        """
        Initialize the GoogleService.
        """
        self.client: GoogleCseClient = client or GoogleCseClient()
        self.expander: QueryExpander = expander or QueryExpander()

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
        expanded_queries: list[str] = self.expander.expand(queries=queries)
        all_candidates: dict[str, JobPosting] = {}

        for window in self._SEARCH_WINDOWS:
            if len(all_candidates) >= max_results:
                logger.info(f"Sufficient candidates found ({len(all_candidates)}). Stopping search.")
                break

            date_filter: str = build_time_filter(days=window)
            window_label: str = f"from last {window} days" if window else "no time filter"
            logger.info(f"🔎 Searching jobs ({window_label})...")

            for query in expanded_queries:
                try:
                    raw_items: list[dict] = self.client.search(query=query, date_filter=date_filter)

                    for item in raw_items:
                        job: JobPosting = from_google_cse_item(item=item)
                        if job.link and job.link not in all_candidates and InitialJobFilter.should_keep(job=job):
                            all_candidates[job.link] = job

                except requests.RequestException as e:
                    logger.warning(f"Failed to fetch query '{query}': {e}")
                    continue

        final_results: list[JobPosting] = list(all_candidates.values())
        return final_results[:max_results]
