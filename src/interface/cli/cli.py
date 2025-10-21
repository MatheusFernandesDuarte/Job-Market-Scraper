# src/interface/cli/cli.py

import itertools
import logging
import sys
from argparse import Namespace

from src.core.builders.query_builder import build_query
from src.core.contracts.job_search_interface import JobSearchInterface
from src.core.logging_config import setup_logging
from src.core.use_cases.job_search_and_enrich_use_case import JobSearchAndEnrichUseCase
from src.interface.cli import args as cli_args
from src.interface.cli import ui as cli_ui
from src.models.job_model import JobPosting
from src.services.google.service import GoogleService
from src.services.scraping.playwright_scraper import PlaywrightScraper

logger = logging.getLogger(__name__)


async def main(argv: list[str] | None = None) -> int:
    """
    Asynchronously orchestrates the command-line application flow.

    This function coordinates parsing arguments, building queries, calling the
    search service, and displaying the output.

    Args:
        argv (list[str] | None): A list of command-line arguments.
            If None, `sys.argv[1:]` is used.

    Returns:
        int: An exit code. `0` for success, non-zero for errors.
    """
    setup_logging()

    cli_arguments: list[str] = argv if argv is not None else sys.argv[1:]
    args: Namespace = cli_args.parse_args(argv=cli_arguments)

    if not (any(loc.strip() for loc in args.locations) or any(sen.strip() for sen in args.seniority) or any(role.strip() for role in args.role)):
        cli_ui.display_error(message="Please provide at least one search criterion.")
        return 1

    combinations: itertools.product = itertools.product(args.locations, args.seniority, args.role)
    queries: list[str] = [query for combo in combinations if (query := build_query(*combo)) is not None]

    if not queries:
        cli_ui.display_error(message="Could not build any valid queries from the provided terms.")
        return 1

    logger.info(cli_ui.display_search_header(queries=queries))

    try:
        async with PlaywrightScraper() as page_scraper:
            search_service: JobSearchInterface = GoogleService()
            use_case: JobSearchAndEnrichUseCase = JobSearchAndEnrichUseCase(
                search_service=search_service,
                page_scraper=page_scraper,
            )

            results: list[JobPosting] = await use_case.execute(queries=queries, max_results=args.max)

    except Exception as exc:
        logger.info(cli_ui.display_error(message=f"An error occurred during the search: {exc}"))
        return 2

    logger.info(cli_ui.display_results(results=results))
    return 0
