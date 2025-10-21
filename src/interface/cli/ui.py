# src/interface/cli/ui.py

"""
UI helper module for displaying all command-line interface feedback.

This module is responsible for printing headers, results, and errors,
ensuring that the core application logic remains decoupled from the
console output.
"""

from src.interface.cli.styler import Styler
from src.models.job_model import JobPosting


def display_search_header(queries: list[str]) -> None:
    """
    Display a header listing the search queries that will be executed.

    Args:
        queries (list[str]): A list of the formatted query strings to be
            printed to the console.

    Returns:
        None
    """
    print(Styler.title(text="Running searches for:"))
    for query in queries:
        print(f"  - {Styler.info(text=query)}")


def display_results(results: list[JobPosting]) -> None:
    """
    Format and display the final list of job posting results.

    If the list is empty, a "No results found" message is shown.

    Args:
        results (list[dict]): A list of dictionaries, where each dictionary
            represents a unique, filtered job posting.

    Returns:
        None
    """
    if not results:
        print(Styler.warning(text="No results found."))
        return

    print(f"\n{Styler.title(text='Top job postings:')}")
    print("-" * 50)

    for i, job in enumerate(iterable=results, start=1):
        print(f"{Styler.success(text=f'{i}. {job.title}')}")
        print(f"   Source: {Styler.dim(text=job.source)}")
        print(f"   Link: {Styler.info(text=job.link)}")

        if job.full_description:
            description_preview: str = job.full_description[:250] + "..."
        else:
            description_preview: str = "Description not available (scraping may have failed)."

        print(f"   Description Preview: {description_preview}\n")


def display_error(message: str) -> None:
    """
    Print a standardized error message to the console.

    Args:
        message (str): The error message to be displayed.

    Returns:
        None
    """
    print(Styler.error(text=f"[error] {message}"))
