# backend/src/core/filters/initial_job_filter.py

import tldextract

from src.models.job_model import JobPosting

NON_TECH_ROLE_KEYWORDS: set[str] = {
    "administrativo",
    "administrativa",
    "administrative",
    "business analyst",
    "analista de negócios",
    "rh",
    "human resources",
    "recursos humanos",
    "recruiter",
    "recrutador",
    "talent acquisition",
    "marketing",
    "sales",
    "vendas",
    "financeiro",
    "financial",
    "analista financeiro",
    "customer support",
    "customer service",
    "atendimento ao cliente",
    "suporte ao cliente",
    "designer",
    "ui/ux",
    "logística",
    "logistics",
    "operations",
    "operações",
    "facilities",
}
EXCLUSION_KEYWORDS: set[str] = {
    # Courses / Education
    "curso",
    "training",
    "bootcamp",
    "certification",
    "masterclass",
    "udemy",
    "coursera",
    "udacity",
    "pluralsight",
    # Forums / Discussions
    "forum",
    "review",
    "discussion",
    "community",
    "thread",
    "perguntas",
    "respostas",
    "questions",
    "answers",
    # Articles / Guides
    "learn",
    "tutorial",
    "guide",
    "examples",
    "example",
    "cheatsheet",
    "how to",
    "what is",
    "interview",
    "aprender",
    "guia",
    "exemplos",
    "notícia",
    "artigo",
    # Spanish
    "aprender",
    "ejemplos",
    "guia",
    "preguntas",
    "respuestas",
}
NOISE_DOMAINS: set[str] = {
    "youtube.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "reddit.com",
    "github.com",
    "gitlab.com",
    "pypi.org",
    "wikipedia.org",
    "quora.com",
    "phpjobs.live",
}


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
            extracted = tldextract.extract(link)
            if not extracted.suffix:
                return extracted.domain
            return f"{extracted.domain}.{extracted.suffix}"
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
        domain: str = InitialJobFilter._get_domain(link=job.link)

        if not domain:
            return False
        if domain in NOISE_DOMAINS:
            return False

        title_lower: str = job.title.lower()
        if any(keyword in title_lower for keyword in NON_TECH_ROLE_KEYWORDS):
            return False

        text_content: str = f"{job.title} {job.snippet}".lower()
        if any(keyword in text_content for keyword in EXCLUSION_KEYWORDS):
            return False

        return True
