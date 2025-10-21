# src/core/filters/initial_job_filter.py

from urllib.parse import ParseResult, urlparse

from src.models.job_model import JobPosting

EXCLUSION_KEYWORDS = {"curso", "training", "salaries", "salary", "review", "forum", "jobs", "vagas"}
NOISE_DOMAINS = {"youtube.com", "facebook.com", "twitter.com", "x.com", "reddit.com"}


class InitialJobFilter:
    """
    Performs a cheap, initial filtering on job postings based on search metadata.
    """

    def _get_domain(link: str) -> str:
        """
        Extract the parent domain from a full URL.

        For example, 'jobs.google.com' becomes 'google.com'.

        Args:
            link (str): The full URL to parse.

        Returns:
            str: The extracted parent domain, or an empty string if parsing fails.
        """
        try:
            parsed_uri: ParseResult = urlparse(url=link)
            domain_parts: list[str] = parsed_uri.netloc.split(sep=".")
            if len(domain_parts) > 1:
                return f"{domain_parts[-2]}.{domain_parts[-1]}"
            return parsed_uri.netloc
        except Exception:
            return ""

    @staticmethod
    def should_keep(job: JobPosting) -> bool:
        """
        Determines if a job posting should be kept for the expensive scraping step.

        Args:
            job (JobPosting): The job posting with initial data (title, snippet).

        Returns:
            bool: True if the job passes the initial filter, False otherwise.
        """
        domain = InitialJobFilter._get_domain(link=job.link)
        if domain in NOISE_DOMAINS:
            return False

        text_content = (job.title + job.snippet).lower()
        if any(keyword in text_content for keyword in EXCLUSION_KEYWORDS):
            return False

        return True
