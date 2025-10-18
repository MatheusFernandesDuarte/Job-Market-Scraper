# src/models/job_model.py

from dataclasses import dataclass, field


@dataclass
class JobPosting:
    """Represents a single job posting."""

    title: str
    link: str
    snippet: str
    source: str
    date: str | None = None
    score: int = field(default=0, repr=False)
