# Job Market Scraper

**Job Market Scraper** is a focused, production-oriented MVP that automates the discovery of international job postings by composing targeted Google search queries and retrieving results via the **Google Custom Search (CSE) API**. This repository demonstrates a pragmatic, extensible approach to job market intelligence suitable for inclusion in a technical portfolio.

---

## Executive summary

This project addresses a common manual workflow: searching for remote or international roles using specific combinations of terms (location/flexibility, seniority, role). The MVP automates that first step — query composition and result collection — and exposes a CLI entrypoint so the workflow can be executed reproducibly.

Key design goals:

- Minimal, testable core (MVP) with clear extension points.
- Deterministic output for easy enrichment and downstream processing.
- Safe handling of API credentials and predictable HTTP behavior.

---

## What this repository contains

- `run.py` — lightweight entry file that invokes the CLI.
- `src/interface/cli/cli.py` — command-line orchestration (builds queries, executes search, prints results).
- `src/core/builders/query_builder.py` — composes search queries in the format: `"{location}" + "{seniority}" + "{role}"`.
- `src/core/factories/service_factory.py` — creates provider instances (currently Google).
- `src/services/google/client.py` — Google CSE HTTP client (requests.Session).
- `src/services/google/mapper.py` — maps raw Google CSE items into domain model.
- `src/services/google/service.py` — provider implementation that paginates queries, deduplicates by link and filters results.
- `src/models/job_model.py` — domain data class `JobPosting`.
- `.env.example` — environment variables template.

---

## Requirements & supported environment

- Python 3.11+ (type hints and dataclasses targeted to 3.11)
- A valid Google Custom Search Engine configured to surface job results (CSE ID) and an API key.

The repository contains a `pyproject.toml` and a lock file. The author uses `uv` as the run/task runner in their workflow — instructions below reflect that.

---

## Installation (recommended)

1. Clone the repository:

```bash
git clone https://github.com/your-username/job-market-scraper.git
cd job-market-scraper
```

2. Create and activate a virtual environment:

```python
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows (PowerShell)
```

3. Install dependencies:

```python
pip install -r requirements.txt
```

4. Create .env file (see .env.example):

```python
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CX=your_custom_search_engine_id_here
```

## Usage

#### Two supported ways to run the CLI:

1. **Using uv (author's workflow)**

If you manage run tasks with uv (project includes uv.lock), you can run the CLI via:

```bash
uv run run.py -- --location "remote" --seniority "Junior" --role "Data Science" --max 20 --date-filter qdr:w
```

- Note: uv run run.py -- passes flags through to the script. Adjust depending on your uv configuration.

2. **Direct Python execution (fallback)**

```python
python run.py --location "remote" --seniority "Junior" --role "Data Science" --max 20 --date-filter qdr:w
```

## Example query composition

The query builder formats terms as quoted tokens and joins them with +:

```arduino
"remote" + "Junior" + "Data Science"
```

This mirrors the strategy you described in the project brief: combine location/flexibility terms + seniority + role to surface international opportunities.

## CLI flags (representative)

The project exposes a CLI (src/interface/cli/cli.py). Common flags (example) include:

- --location — e.g., "remote", "latam", "brazil", "work from anywhere"
- --seniority — e.g., "Junior", "Mid", "Senior"
- --role — e.g., "Data Science", "Software Engineer"
- --max — maximum number of returned postings
- --date-filter — reduce results by recency (e.g., qdr:d, qdr:w, qdr:m — mapped internally)

Refer to the CLI source for the exact, authoritative argument names and options.

## Architecture notes & rationale

- **Separation of concerns:** query building, provider creation, HTTP client and mapping are explicit modules to facilitate testing and future provider additions (e.g., Bing, SerpAPI).
- **Deterministic mapping:** from_google_cse_item normalizes the raw JSON into a JobPosting dataclass. This makes downstream enrichment and deduplication straightforward.
- **Session reuse:** GoogleCseClient uses a persistent requests.Session with a default timeout to limit resource churn.
- **Defensive environment handling:** the client throws a RuntimeError early if API credentials are missing, preventing accidental leaked calls.

## Notable implementation details (observed)

- `src/services/google/client.py` calls Google CSE v1 endpoint and exposes a `search(query, date_filter=None)` method returning the `items` list or an empty list.
- `src/services/google/service.py` orchestrates multiple searches, deduplication by link and final filtering using `JobFilter` and `search_time_filter`.
- `src/models/job_model.py` defines a compact `JobPosting` dataclass with `title`, `link`, `snippet`, `source`, `date`, and an internal `score`.

### Author & contact

Matheus — Software Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/seu-matthfeeer)
