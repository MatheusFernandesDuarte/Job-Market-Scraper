# backend/src/interface/api/fastapi_app.py

import asyncio
import itertools
import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.core.builders.query_builder import build_query
from src.core.contracts.job_search_interface import JobSearchInterface
from src.core.use_cases.job_search_and_enrich_use_case import JobSearchAndEnrichUseCase
from src.interface.api.schemas import JobResponse, MatchRequest
from src.services.google.service import GoogleService
from src.services.scraping.playwright_scraper import PlaywrightScraper

logger = logging.getLogger(__name__)

# Fix Windows event loop policy
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception as e:
        logger.warning(f"Could not set WindowsSelectorEventLoopPolicy: {e}")

app = FastAPI(title="Job Market Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_queries(payload: MatchRequest) -> list[str]:
    locations = payload.location if payload.location else [""]
    seniorities = [payload.seniority] if payload.seniority else [""]
    techs = payload.tech_stack if payload.tech_stack else [""]
    combinations = itertools.product(locations, seniorities, techs)
    return [q for combo in combinations if (q := build_query(*combo))]


@app.post("/api/search", response_model=list[JobResponse])
async def match_jobs(payload: MatchRequest):
    """
    Receives user profile and returns ranked job list.
    """
    if not (payload.tech_stack or payload.location or payload.seniority):
        raise HTTPException(status_code=400, detail="At least one criterion is required.")

    queries = _build_queries(payload)

    if not queries:
        raise HTTPException(status_code=400, detail="No valid query generated.")

    try:
        async with PlaywrightScraper() as scraper:
            search_service: JobSearchInterface = GoogleService()
            use_case = JobSearchAndEnrichUseCase(
                search_service=search_service,
                page_scraper=scraper,
            )
            jobs = await use_case.execute(queries=queries, max_results=10)
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {exc}")

    return [
        JobResponse(
            title=job.title,
            company=getattr(job, "company", None),
            url=getattr(job, "link", None),
            match_score=getattr(job, "score", None),
            salary=getattr(job, "salary", None),
            experience=getattr(job, "experience", None),
            date_posted=getattr(job, "date", None),
            tags=getattr(job, "tags", None),
        )
        for job in jobs
    ]
