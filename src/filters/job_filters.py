# src/filters/job_filters.py

from collections.abc import Iterable
from urllib.parse import ParseResult, urlparse

from src.models.job_model import JobPosting

GOOD_DOMAINS: set[str] = {
    "linkedin.com",
    "indeed.com",
    "glassdoor.com",
    "lever.co",
    "greenhouse.io",
    "workday.com",
    "gupy.io",
    "remotive.com",
    "weworkremotely.com",
}
NOISE_DOMAINS: set[str] = {
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "reddit.com",
    "researchgate.net",
    "sciencedirect.com",
    "toptal.com",
}
JOB_KEYWORDS: set[str] = {
    "vaga",
    "job",
    "hiring",
    "career",
    "oportunidade",
    "developer",
    "engineer",
    "analyst",
    "apply",
    "recruitment",
    "vacancy",
    "trabalhe conosco",
}
EXCLUSION_KEYWORDS: set[str] = {"curso", "training", "template", "example", "exemplo"}


class JobFilter:
    """
    A class to filter and score job postings based on a defined set of rules.
    """

    def _get_domain(self, link: str) -> str:
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

    def calculate_score(self, job_posting: JobPosting) -> int:
        """
        Calculate a relevance score for a single job posting.

        The score is determined by applying positive weights for job-related
        keywords and trusted domains, and negative weights for noise.

        Args:
            job_posting (JobPosting): The job posting object to be scored.

        Returns:
            int: A numerical score. Higher scores indicate greater relevance.
        """
        score: int = 0
        text_content: str = (job_posting.title + job_posting.snippet).lower()
        domain: str = self._get_domain(link=job_posting.link)

        if any(keyword in text_content for keyword in JOB_KEYWORDS):
            score += 2

        if domain in GOOD_DOMAINS:
            score += 3
        elif domain in NOISE_DOMAINS:
            score -= 5

        if any(keyword in text_content for keyword in EXCLUSION_KEYWORDS):
            score -= 5

        return score

    def process(self, results: Iterable[JobPosting]) -> list[JobPosting]:
        """
        Process an iterable of job postings to score, filter, and sort them.

        Only job postings with a score greater than zero are kept. The final
        list is sorted in descending order of relevance.

        Args:
            results (Iterable[JobPosting]): An iterable of JobPosting objects.

        Returns:
            list[JobPosting]: A sorted and filtered list of the most relevant
            job postings.
        """
        scored_jobs: list[JobPosting] = []
        for job in results:
            score: int = self.calculate_score(job_posting=job)
            if score > 0:
                job.score = score
                scored_jobs.append(job)

        scored_jobs.sort(key=lambda job: job.score, reverse=True)
        return scored_jobs
