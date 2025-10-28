from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

import backend.src.interface.api.fastapi_app as api_module

client = TestClient(api_module.app)


class DummyScraper:
    """Mock for PlaywrightScraper that doesn't open a browser."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummyUseCase:
    """Mock for the use case that simulates job search and enrichment."""

    def __init__(self, *args, **kwargs):
        pass

    async def execute(self, queries, max_results):
        return [
            SimpleNamespace(
                title="Python Developer",
                company="Acme Corp",
                link="https://example.com/job/1",
                score=0.95,
                salary="R$ 8.000",
                experience="2+ anos",
                date="2025-10-01",
                tags=["python", "backend"],
            )
        ]


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    """Patches external dependencies before each test."""
    monkeypatch.setattr(api_module, "PlaywrightScraper", DummyScraper)
    monkeypatch.setattr(api_module, "JobSearchAndEnrichUseCase", DummyUseCase)


def test_search_valid_request():
    """Should return a valid job list when a correct payload is sent."""
    payload = {"tech_stack": ["Python"], "location": ["remote"], "seniority": "Junior"}
    response = client.post("/api/search", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    job = data[0]
    assert job["title"] == "Python Developer"
    assert job["company"] == "Acme Corp"
    assert job["salary"] == "R$ 8.000"


def test_search_no_criteria():
    """Should return 400 error when no criteria are provided."""
    payload = {"tech_stack": [], "location": [], "seniority": None}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 400
    assert "At least one criterion" in response.text


def test_search_no_queries(monkeypatch):
    """Should return 400 error when _build_queries generates no queries."""

    def dummy_build_queries(payload):
        return []

    monkeypatch.setattr(api_module, "_build_queries", dummy_build_queries)

    payload = {"tech_stack": ["Python"], "location": ["remote"], "seniority": "Junior"}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 400
    assert "No valid query" in response.text


def test_search_internal_error(monkeypatch):
    """Should return 500 error if the use case raises an exception."""

    class FailingUseCase:
        async def execute(self, queries, max_results):
            raise RuntimeError("Test error")

    monkeypatch.setattr(api_module, "JobSearchAndEnrichUseCase", FailingUseCase)

    payload = {"tech_stack": ["Python"], "location": ["remote"], "seniority": "Junior"}
    response = client.post("/api/search", json=payload)

    assert response.status_code == 500
    assert "Failed to fetch jobs" in response.text
