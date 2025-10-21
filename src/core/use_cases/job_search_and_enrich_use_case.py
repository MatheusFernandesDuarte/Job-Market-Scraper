# src/core/use_cases/job_search_and_enrich_use_case.py

import asyncio
import logging
from typing import ClassVar

from src.core.contracts.job_search_interface import JobSearchInterface
from src.core.contracts.page_scraper_interface import PageScraperInterface
from src.core.filters.initial_job_filter import InitialJobFilter
from src.core.validators.job_validator import JobValidator
from src.models.job_model import JobPosting

logger = logging.getLogger(__name__)


class JobSearchAndEnrichUseCase:
    """
    Orchestrates an iterative pipeline to find, enrich, and validate jobs
    until a target number of high-quality results is met.

    This class is the core orchestrator of the application's business logic.
    It fetches a large pool of candidates and processes them in smaller,
    concurrent batches to efficiently produce a curated list of relevant
    job postings.
    """

    _CANDIDATE_POOL_SIZE: ClassVar[int] = 40
    _ENRICHMENT_BATCH_SIZE: ClassVar[int] = 10

    def __init__(
        self,
        search_service: JobSearchInterface,
        page_scraper: PageScraperInterface,
    ) -> None:
        """
        Initializes the use case with its dependencies.

        Args:
            search_service (JobSearchInterface): A service for finding jobs
                from an external source like the Google API.
            page_scraper (PageScraperInterface): An async service for scraping
                and extracting content from web pages.
        """
        self._search_service = search_service
        self._page_scraper = page_scraper

    async def execute(self, queries: list[str], max_results: int) -> list[JobPosting]:
        """
        Executes a dynamic pipeline that processes job candidates in batches.

        This method orchestrates a four-step process:
        1. Fetches a large pool of initial job candidates.
        2. Applies a cheap, initial filter to remove obvious non-job results.
        3. Concurrently enriches the filtered jobs in batches with full descriptions.
        4. Applies a final validation to each enriched job and collects them
           until the desired number of results (`max_results`) is reached.

        Args:
            queries (list[str]): A list of search query strings to execute.
            max_results (int): The target number of high-quality job postings
                to return.

        Returns:
            list[JobPosting]: A final, curated list of high-quality, validated
                              job postings, sliced to `max_results`.
        """
        logger.info("Starting dynamic job processing pipeline...")

        initial_candidates: list[JobPosting] = self._search_service.search(queries=queries, max_results=self._CANDIDATE_POOL_SIZE)
        logger.info(f"Fetched {len(initial_candidates)} initial candidates.")

        filtered_pool: list[JobPosting] = [job for job in initial_candidates if InitialJobFilter.should_keep(job=job)]
        logger.info(f"Initial filter reduced pool to {len(filtered_pool)} candidates.")

        validated_jobs: list[JobPosting] = []

        for i in range(0, len(filtered_pool), self._ENRICHMENT_BATCH_SIZE):
            if len(validated_jobs) >= max_results:
                logger.info("Target number of validated jobs reached. Stopping early.")
                break

            batch: list[JobPosting] = filtered_pool[i : i + self._ENRICHMENT_BATCH_SIZE]
            logger.info(f"Processing batch {i // self._ENRICHMENT_BATCH_SIZE + 1} with {len(batch)} jobs...")

            tasks = [self._page_scraper.fetch_content(job.link) for job in batch]
            descriptions: list[str] = await asyncio.gather(*tasks)

            enriched_batch: list[JobPosting] = batch
            for job, description in zip(enriched_batch, descriptions):
                job.full_description = description

            newly_validated: list[JobPosting] = [job for job in enriched_batch if JobValidator.is_valid(job=job)]
            validated_jobs.extend(newly_validated)
            logger.info(f"Found {len(newly_validated)} valid jobs in this batch. Total valid: {len(validated_jobs)}")

        return validated_jobs[:max_results]
