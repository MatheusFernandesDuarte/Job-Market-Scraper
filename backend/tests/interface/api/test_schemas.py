# backend/tests/interface/api/test_schemas.py

import pytest
from pydantic import ValidationError

from backend.src.interface.api.schemas import JobResponse, MatchRequest


def test_match_request_valid():
    valid_data = {"tech_stack": ["Python", "FastAPI"], "location": ["remote"], "seniority": "Senior"}
    req = MatchRequest(**valid_data)
    assert req.tech_stack == valid_data["tech_stack"]
    assert req.location == valid_data["location"]
    assert req.seniority == valid_data["seniority"]


def test_match_request_missing_optional():
    valid_data = {
        "tech_stack": ["Python"],
        "location": ["remote"],
        # seniority omitted, should default to None
    }
    req = MatchRequest(**valid_data)
    assert req.seniority is None


def test_match_request_invalid_types():
    invalid_data = {
        "tech_stack": "Python",  # Should be list
        "location": "remote",
    }
    with pytest.raises(ValidationError):
        MatchRequest(**invalid_data)


def test_job_response_fields():
    data = {
        "title": "Developer",
        "company": "Acme Inc",
        "url": "https://example.com/job/1",
        "match_score": 0.95,
        "skills_matched": ["python", "fastapi"],
        "skills_missing": ["docker"],
        "salary": "$100k",
        "experience": "3 years",
        "date_posted": "2025-10-01",
        "tags": ["remote", "full-time"],
    }
    job = JobResponse(**data)
    for field, value in data.items():
        assert getattr(job, field) == value


def test_job_response_optional_fields_none():
    job = JobResponse(title="Developer")
    assert job.company is None
    assert job.url is None
    assert job.match_score is None
    assert job.skills_matched is None
    assert job.skills_missing is None
    assert job.salary is None
    assert job.experience is None
    assert job.date_posted is None
    assert job.tags is None
