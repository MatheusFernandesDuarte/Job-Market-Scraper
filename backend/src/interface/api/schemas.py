# backend/src/interface/api/schemas.py

from pydantic import BaseModel


class MatchRequest(BaseModel):
    tech_stack: list[str]
    location: list[str]
    seniority: str | None = None


class JobResponse(BaseModel):
    title: str
    company: str | None = None
    url: str | None = None
    match_score: float | None = None
    skills_matched: list[str] | None = None
    skills_missing: list[str] | None = None
    salary: str | None = None
    experience: str | None = None
    date_posted: str | None = None
    tags: list[str] | None = None
