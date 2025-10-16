# JobScraper

## Documentation

- [Epics and Stories Backlog](BACKLOG.md)
This repository currently contains the initial scaffold for the JobScraper project.

## Structure

- `backend/`: Domain-specific packages for ingestion, profiling, analytics, compliance, and more.
- `frontend/`: Placeholder for the future user-facing application.
- `infra/`: Docker and orchestration configuration placeholders.
- `tests/`: Placeholder directory for automated tests.

Each backend package exposes a module-level docstring describing its intended responsibility.
## Goal
- Build an automated pipeline that discovers, extracts, and normalizes job postings from multiple sources.
- Provide a query interface that allows product and data teams to analyze market hiring trends in near real time.

## Success Criteria
- Daily ingestion completes in under one hour with <1% extraction failures per source.
- Stakeholders can filter and export job data by company, role, location, and posting age.
- Monitoring dashboards alert the team of source outages or schema drifts within 15 minutes.

## Tech Stack
- **Backend:** Python 3.11, FastAPI, SQLAlchemy.
- **Data:** PostgreSQL 15, Redis for task coordination, S3 for raw scrape storage.
- **Infrastructure:** Docker, Kubernetes (GKE), Terraform for IaC, GitHub Actions for CI/CD.
- **Observability:** Prometheus, Grafana, OpenTelemetry traces.

## Repository Layout
- `ingestion/`: Source-specific crawlers, parsers, and normalization utilities.
- `api/`: FastAPI service exposing search, filtering, and admin endpoints.
- `db/`: Migrations, seeds, and data-access layer abstractions.
- `infrastructure/`: Terraform modules, Kubernetes manifests, and deployment scripts.
- `docs/`: Architecture diagrams, onboarding guides, and ADRs.
- `scripts/`: Operational tooling (backfills, data quality checks, one-off fixes).

## Environment & Secrets
- Store local environment variables in `.env.local`; never commit secrets.
- Use GitHub Actions secrets for CI/CD credentials and Terraform cloud backends.
- Rotate third-party API keys quarterly and document rotations in `docs/secrets-log.md`.
- Prefer HashiCorp Vault in production for sourcing database and scraper credentials.

## Epics & Stories
- **Epic: Source Onboarding**
  - Implement reusable crawler interface and add connectors for LinkedIn, Indeed, and niche boards.
  - Automate schema validation for new sources with contract tests.
- **Epic: Data Quality & Insights**
  - Build deduplication pipeline and classification models for job titles and skills.
  - Deliver analytics endpoints and dashboards for hiring trend reports.
- **Epic: Platform Reliability**
  - Add observability instrumentation, alerting rules, and runbooks.
  - Harden deployment pipeline with canary rollouts and blue/green fallbacks.

## Data Model
- `jobs`: core posting fields (title, company, location, salary range, post_date, source).
- `job_details`: unstructured descriptions, normalized skills, seniority tags.
- `companies`: metadata including industry, size, headquarters, and external identifiers.
- `pipelines`: ingestion run metadata (status, runtime, failure counts, source).
- Use slowly changing dimensions for company metadata and retain historical job snapshots.

## Milestones
- **M1 – Prototype (Month 1):** Single-source crawler with manual review workflow.
- **M2 – Multi-Source Beta (Month 2):** Add three priority sources, implement dedupe, expose read-only API.
- **M3 – Production Ready (Month 3):** Harden infrastructure, enable alerts, deliver analytics dashboards.

## Non-Functional Requirements
- Achieve 99.5% API uptime with p95 latency under 400 ms.
- Ensure pipelines recover automatically from transient failures and retry up to three times.
- Encrypt data at rest and in transit; comply with SOC 2 logging standards.
- Provide audit trails for edits to job records and configuration changes.

## Risks
- Website anti-bot measures may block crawlers; mitigate with rotating proxies and legal review.
- Schema drift across sources could break normalization; schedule nightly validation runs.
- High ingestion volume may increase infrastructure costs; implement autoscaling and budget alerts.
- Regulatory changes (e.g., GDPR, CCPA) could restrict data use; coordinate with legal quarterly.

## Ask Codex
- Prefer incremental PRs with high test coverage; reference related issues in descriptions.
- Before implementing new sources, search the repo for existing adapters to reuse patterns.
- Use `scripts/dev_bootstrap.sh` to set up local services and seed baseline data.
- Run `make quality` before submitting to catch linting or typing regressions.
