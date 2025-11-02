# backend/src/interface/cli/ui.py

"""
UI helper module for displaying all command-line interface feedback.

This module is responsible for printing headers, results, and errors,
ensuring that the core application logic remains decoupled from the
console output.
"""

from src.interface.cli.styler import Styler
from src.models.job_model import JobPosting


def display_search_header(queries: list[str]) -> str:
    """
    Returns a formatted string listing the search queries to be executed,
    for display in a frontend or outras interfaces textuais.

    Args:
        queries (list[str]): List of formatted query strings.

    Returns:
        str: Formatted text with title and queries listed.
    """
    header: str = Styler.title(text="Running searches for:")
    lines: list[str] = [header] + [f"  - {Styler.info(text=query)}" for query in queries]
    return "\n".join(lines)


def display_results(results: list[JobPosting]) -> str:
    """
    Format and return the final list of job posting results as a string.

    If the list is empty, returns a "No results found" message.

    Args:
        results (list[JobPosting]): A list of JobPosting objects to format.

    Returns:
        str: A formatted string representing the job postings.
    """
    if not results:
        return Styler.warning(text="No results found.")

    lines: list[str] = [f"\n{Styler.title(text='Top job postings:')}", "-" * 50]

    for i, job in enumerate(results, start=1):
        lines.append(f"{Styler.success(text=f'{i}. {job.title}')}")
        lines.append(f"   Source: {Styler.dim(text=job.source)}")
        lines.append(f"   Link: {Styler.info(text=job.link)}")

        if job.full_description:
            description_preview: str = job.full_description[:250] + "..."
        else:
            description_preview: str = "Description not available (scraping may have failed)."

        lines.append(f"   Description Preview: {description_preview}\n")

    return "\n".join(lines)


def display_error(message: str) -> str:
    """
    Return a standardized error message string formatted for display.

    Args:
        message (str): The error message to format.

    Returns:
        str: The formatted error message.
    """
    return Styler.error(text=f"[error] {message}")
