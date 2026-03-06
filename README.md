# JobScraper

Automated pipeline for discovering, extracting, and normalizing job postings across multiple sources — built to surface signal, not volume.

---

## Why I Built This

Job boards are noisy. Most surfaces are optimized for maximum posting volume, which means a search for "Principal PM" returns 200 results where maybe 15 are actually relevant. I wanted a system that could ingest from multiple sources, deduplicate aggressively, classify by actual fit (not just keyword match), and serve a clean query interface for filtering and trend analysis.

This is also the data foundation for a larger job search intelligence system — you can't do meaningful signal detection without clean, normalized posting data underneath it.

---

## What It Does

- Ingests job postings from multiple sources on a daily schedule
- Normalizes across sources (title, company, location, date, requirements) into a consistent schema
- Deduplicates across sources using fuzzy matching on company + title + location
- Classifies postings by role type, seniority, and domain
- Exposes a query API for filtering by company, role, location, and posting age

---

## Design Decisions

**Source adapter pattern.** Each job source (board, RSS feed, direct scrape) implements a common interface. Adding a new source means writing one adapter, not touching the core pipeline. The tradeoff: more upfront abstraction, but it's paid back fast once you have more than two sources behaving differently.

**PostgreSQL over a document store.** Job postings look like unstructured data but the queries are almost always relational (filter by company, sort by date, aggregate by role type). A document store would have made the ingestion side easier and the query side harder. Chose the harder ingestion, cleaner queries.

**Deduplication before classification.** Running classification on duplicates wastes compute and inflates signal. Dedup runs first in the pipeline even though it's more complex to implement pre-classification.

---

## Stack

- **Backend:** Python 3.11, FastAPI
- **Storage:** PostgreSQL

---

## Status

Active development. Greenhouse and Builtin source adapters complete. Multi-source deduplication in progress.
