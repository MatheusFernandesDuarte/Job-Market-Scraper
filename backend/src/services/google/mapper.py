# backend/src/services/google/mapper.py

from typing import Any

from src.models.job_model import JobPosting


def from_google_cse_item(item: dict[str, Any]) -> JobPosting:
    """
    Map a raw dictionary from the Google CSE API to a JobPosting object.

    This function safely extracts data from the nested API response structure
    and populates a structured domain model.

    Args:
        item (dict[str, Any]): A single 'item' dictionary from the Google
            CSE API response.

    Returns:
        JobPosting: A structured JobPosting data object.
    """
    job_posting: JobPosting = JobPosting(
        title=item.get("title", ""),
        link=item.get("link", ""),
        snippet=item.get("snippet", ""),
        source=item.get("displayLink", ""),
        date=item.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time"),
    )
    return job_posting
