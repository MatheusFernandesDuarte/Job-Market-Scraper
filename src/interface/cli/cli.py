# src/interface/cli/cli.py

"""
Main entrypoint for the Job Market Search command-line interface.

This module orchestrates the application flow by parsing arguments,
building queries, executing the search, and displaying results.
"""

import itertools
import sys
from argparse import Namespace

from src.core.builders.query_builder import build_query
from src.core.factories.service_factory import create_service
from src.interface.cli import args as cli_args
from src.interface.cli import ui as cli_ui
from src.models.job_model import JobPosting
from src.services.google.service import GoogleService


def main(argv: list[str] | None = None) -> int:
    """
    Orchestrate the command-line application flow.

    This function coordinates parsing arguments, building queries, calling the
    search service, and displaying the output.

    Args:
        argv (list[str] | None): A list of command-line arguments.
            If None, `sys.argv[1:]` is used.

    Returns:
        int: An exit code. `0` for success, non-zero for errors.
    """
    cli_arguments: list[str] = argv if argv is not None else sys.argv[1:]
    args: Namespace = cli_args.parse_args(argv=cli_arguments)

    if args.locations == [""] and args.seniority == [""] and args.role == [""]:
        cli_ui.display_error("Please provide at least one search criterion (--locations, --seniority, or --role).")
        return 1

    combinations: itertools.product = itertools.product(args.locations, args.seniority, args.role)
    queries: list[str] = [query for combo in combinations if (query := build_query(*combo)) is not None]

    if not queries:
        cli_ui.display_error(message="Could not build any valid queries from the provided terms.")
        return 1

    cli_ui.display_search_header(queries=queries)

    try:
        service: GoogleService = create_service(service_name="google")
        results: list[JobPosting] = service.search(queries=queries, max_results=args.max)
    except Exception as exc:
        cli_ui.display_error(message=f"An error occurred during the search: {exc}")
        return 2

    cli_ui.display_results(results=results)
    return 0
