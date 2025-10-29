# Job Market Scraper — Phased Product Roadmap

## Vision

To evolve the **Job Market Scraper** from a command-line tool into a personalized, data-driven career co-pilot that intelligently matches developers with the best international job opportunities.

---

### **Phase 1: Building the Data Engine & Core API**

**Goal:** To create a robust backend that automatically scrapes, processes, and stores enriched job data, making it available through an API.

* **[X] 1. Implement Job Page Scraper:**
  * Develop a scraper using `Playwright` to visit the job links found by the Google CSE.
  * The primary function is to extract the full, raw text content from each job description page.
* **[ ] 2. Develop a Rule-Based Extraction Engine:**
  * **Tech Stack Extraction:** Create a comprehensive dictionary of technical keywords (languages, frameworks, cloud services, databases). The engine will scan the job text and tag the posting with all matching keywords.
  * **Experience Level Extraction:** Use regular expressions (Regex) to find patterns related to years of experience (e.g., "5+ years", "at least 3 years").
  * **Salary Data Extraction:** Implement Regex patterns to identify and parse salary information (e.g., "$120k - $140k/year", "€70,000"). Normalize this data into a common format (e.g., annual USD).
* **[X] 3. Build the Core API:**
  * Develop a RESTful API using **FastAPI** to serve the processed job data.
  * Create endpoints like `/jobs` to list all available positions and `/jobs/{id}` to retrieve details for a single job.

---

### **Phase 2: The Personalized User Experience**

**Goal:** To build a user-facing web interface that allows developers to define their profile and receive a ranked list of job opportunities tailored to them.

* **[X] 1. Create the User Profile Interface:**
  * Build a simple web form where users can input their professional profile.
  * **Required Fields:**
    * **Tech Stack:** A simple text input where the user can type their skills, separated by commas (e.g., Python, React, AWS, Docker).
    * **Location:** A simple text input where the user can type the location they want to work.
    * **Seniority Level:** A dropdown (e.g., Junior, Mid-level, Senior, Staff).
* **[ ] 2. Design the Matching Algorithm:**
  * Develop a multi-factor scoring engine to quantify job-to-user profile fit based on structured attributes.
  * Core scoring components:
    * **Tech Stack Overlap:** Compute the ratio of matching technologies between user skills and job requirements. Assign a high weight to this metric as it drives relevance.
    * **Experience Compatibility:** Calculate a weighted score based on the difference between user experience (years) and the job’s required experience to penalize unsuitable matches.
    * **Seniority Alignment:** Map seniority levels to numeric tiers and evaluate alignment to reward close matches.
  * The matching system should produce a **Match Score** expressed as a percentage or normalized float ranking all jobs per user query.
  * Implementation considerations:
    * Use modular and configurable weights to allow tuning based on user feedback or A/B testing.
    * Support future integration of additional signals such as location preference, salary expectations, and soft skills.
    * Ensure efficient computation at scale by implementing indexes or caching as needed.
  * Output the scores alongside job metadata for downstream presentation in the ranked results dashboard.
* **[X] 3. Develop the Ranked Results Dashboard:**
  * After the user provides their profile and initiates a search, display the results in a clean, sortable table.
  * The table will be ranked by **Match Score** by default and include the following columns:
    * **Match Score:** e.g., "95%".
    * **Job Title & Company:** With a link to the original posting.
    * **Your Skill Overlap:** A visual summary showing which of the user's skills matched (e.g., `Matched: Python, AWS | Missing: Kubernetes`). This is a key feature.
    * **Salary Range:** The extracted and normalized salary.
    * **Required Experience:** The extracted years of experience.
    * **Date Posted:** To prioritize recent opportunities.

---

### **Phase 3: Automation & Market Intelligence**

**Goal:** To make the platform proactive and transform the collected data into valuable market insights for the developer community.

* **[ ] 1. Implement Automated Scans:**
  * Use a scheduler library like `APScheduler` or a system `cron` job to run the scraping and processing pipeline automatically at regular intervals (e.g., every 6 hours).
* **[ ] 2. Create Proactive Job Alerts:**
  * Allow users to "save" their search and subscribe to alerts.
  * Implement a notification system (e.g., via email or Discord/Slack webhooks) that sends a message when a new job with a high Match Score (e.g., >85%) is found.
* **[ ] 3. Build a Market Insights Page:**
  * Leverage the historical data in your database to create a public dashboard with analytics.
  * Display simple charts and stats that answer questions like:
    * "Top 10 most in-demand remote technologies this month."
    * "Average salary range for Senior Software Engineers in LATAM."
    * "Trend of demand for 'Go' vs. 'Rust' over the last 6 months."

### Author & contact

Matheus — Software Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matthfeeer)
