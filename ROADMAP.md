
# Job Market Scraper — Roadmap

This document outlines a checklist of potential features and improvements to evolve the MVP into a more robust and feature-rich job intelligence tool.

## Future Enhancements & Ideas

### Backend & Data

* [ ] **Database Persistence:** Migrate from in-memory processing to a persistent database (e.g., SQLite or PostgreSQL) to store and query historical job data.
* [ ] **Smarter Deduplication:** Implement more advanced logic to identify duplicate jobs (e.g., canonicalize URLs, use a hash of the title and company).
* [ ] **Date Parsing & Normalization:** Parse publication dates from job snippets and normalize them to a standard ISO 8601 format.
* [ ] **Support for More Providers:** Add new service providers for other job boards (e.g., Indeed, LinkedIn directly).
* [ ] **Pagination Support:** Implement logic to fetch multiple pages of results from a single provider query.
* [ ] **Resilient API Calls:** Add retry logic with exponential backoff for API requests to handle transient network errors.
* [ ] **Keyword Expansion:** Use NLP or synonym lists to expand user queries for more comprehensive results (e.g., "dev" -> "developer", "engineer").
* [ ] **AI-Powered Ranking:** Develop a more sophisticated ranking model to surface the most relevant roles based on user profiles or preferences.

### Frontend & User Experience

* [ ] **Web API:** Create a RESTful API using FastAPI to expose the collected job data.
* [ ] **Web Dashboard:** Build a simple web frontend (e.g., using React or Vue) to display saved searches, view results, and manage settings.
* [ ] **User Authentication:** Add authentication (e.g., OAuth2 or API tokens) to support multiple users.
* [ ] **Structured Logging:** Implement structured logging to make debugging and monitoring easier.
* [ ] **Enhanced CLI Output:** Improve the CLI with more flags (e.g., `--verbose`) and better-formatted outputs.

### DevOps & Integrations

* [ ] **Scheduled Scans:** Add a lightweight scheduler (e.g., cron-based or using a library like `APScheduler`) to run searches automatically.
* [ ] **Pre-commit Hooks:** Set up pre-commit hooks for automated code formatting (Black, isort) and linting (Ruff, Mypy) to improve code quality.
* [ ] **Data Export:** Add CLI subcommands to export search results to common formats like CSV or JSON.
* [ ] **Real-time Notifications:** Implement a notification system to send alerts for new, matching jobs via webhooks (e.g., Slack, Discord).
* [ ] **Productivity Tool Integrations:** Build direct integrations to send job data to tools like Google Sheets or Notion.


### Author & contact

Matheus — Software Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/seu-matthfeeer)
