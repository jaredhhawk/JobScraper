"""Client for Greenhouse job board API."""
from __future__ import annotations

from typing import Any, Dict, Iterable

from .base import BaseJobSourceClient


class GreenhouseJobSourceClient(BaseJobSourceClient):
    """Integration for retrieving jobs from the Greenhouse job board."""

    source_name = "greenhouse"
    endpoint = "/greenhouse/jobs"
    field_mapping = {
        "id": "id",
        "title": "title",
        "company_name": lambda job: job.get("metadata", {}).get("company"),
        "location": "location.name",
        "url": "absolute_url",
        "description": "content",
    }

    def fetch_jobs(self, profile: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        params = {
            "query": " ".join(profile.get("role_keywords", [])),
            "levels": ",".join(profile.get("seniority", [])),
            "departments": ",".join(profile.get("industries", [])),
        }
        filtered_params = {key: value for key, value in params.items() if value}
        return self._paginate(self.endpoint, filtered_params)
