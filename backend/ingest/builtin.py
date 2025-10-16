"""Client for the built-in job aggregation API."""
from __future__ import annotations

from typing import Any, Dict, Iterable

from .base import BaseJobSourceClient


class BuiltinJobSourceClient(BaseJobSourceClient):
    """Fetch job postings from the internal job aggregation service."""

    source_name = "builtin"
    endpoint = "/jobs"
    field_mapping = {
        "id": "id",
        "title": "title",
        "company_name": "company",
        "location": "location",
        "url": "apply_link",
        "description": "description",
    }

    def fetch_jobs(self, profile: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        params = {
            "keywords": ",".join(profile.get("role_keywords", [])),
            "seniority": ",".join(profile.get("seniority", [])),
            "industries": ",".join(profile.get("industries", [])),
        }
        filtered_params = {key: value for key, value in params.items() if value}
        return self._paginate(self.endpoint, filtered_params)
