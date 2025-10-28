# backend/src/core/validators/job_validator.py

from __future__ import annotations

import logging
from typing import ClassVar

from backend.src.models.job_model import JobPosting

logger = logging.getLogger(__name__)


class JobValidator:
    """
    A utility class to validate the quality and relevance of a JobPosting.
    """

    _FORBIDDEN_TITLE_KEYWORDS: ClassVar[list[str]] = ["jobs", "salaries", "salary", "vagas", "salários"]
    _FORBIDDEN_CONTENT_PHRASES: ClassVar[list[str]] = [
        "verifying you are human",
        "review the security of your connection",
        "enable javascript and cookies",
        "lorem ipsum",
        "pellentesque habitant",
    ]
    _REQUIRED_CONTENT_KEYWORDS: ClassVar[list[str]] = [
        "responsibilities",
        "requirements",
        "qualifications",
        "experience",
        "skills",
        "duties",
        "about the role",
        "your role",
        "responsabilidades",
        "requisitos",
        "qualificações",
        "experiência",
    ]
    _MIN_DESCRIPTION_LENGTH: ClassVar[int] = 200

    @staticmethod
    def is_valid(job: JobPosting) -> bool:
        """
        Checks if a job posting meets the minimum quality criteria.

        This method applies a series of rules to filter out irrelevant pages,
        bot-check pages, job lists, and postings with low-quality content.

        Args:
            job (JobPosting): The job posting to validate.

        Returns:
            bool: True if the job is valid, False otherwise.
        """
        # Rule 1: Must have a description of a minimum length.
        if not job.full_description or len(job.full_description) < JobValidator._MIN_DESCRIPTION_LENGTH:
            logger.debug(f"INVALID job (short/no description): {job.title}")
            return False

        # Rule 2: Title should not indicate a list or salary page.
        title_lower = job.title.lower()
        if any(keyword in title_lower for keyword in JobValidator._FORBIDDEN_TITLE_KEYWORDS):
            logger.debug(f"INVALID job (forbidden title keyword): {job.title}")
            return False

        # Rule 3: Content should not contain bot-check or placeholder phrases.
        description_lower = job.full_description.lower()
        if any(phrase in description_lower for phrase in JobValidator._FORBIDDEN_CONTENT_PHRASES):
            logger.debug(f"INVALID job (forbidden content phrase): {job.title}")
            return False

        # Rule 4: Content MUST contain at least one common job description keyword.
        if not any(keyword in description_lower for keyword in JobValidator._REQUIRED_CONTENT_KEYWORDS):
            logger.debug(f"INVALID job (missing required keywords): {job.title}")
            return False

        logger.info(f"VALID job found: {job.title}")
        return True

