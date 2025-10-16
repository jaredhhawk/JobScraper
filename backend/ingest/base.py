"""Base classes and helpers for job source ingestion clients."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, Iterator, List, MutableMapping, Optional


RequestCallable = Callable[[str, str, Optional[MutableMapping[str, Any]], Optional[MutableMapping[str, str]]], Dict[str, Any]]


class BaseJobSourceClient(ABC):
    """Shared functionality for job source ingestion clients.

    This class standardises authentication, pagination, and normalisation for
    vendor specific job source integrations. Sub-classes are expected to
    implement :meth:`fetch_jobs` using the pagination helpers and to provide a
    :pyattr:`field_mapping` describing how to translate raw records into the
    normalised job schema.
    """

    source_name: str = "base"
    result_key: str = "results"
    field_mapping: Dict[str, Any] = {
        "id": "id",
        "title": "title",
        "company_name": "company",
        "location": "location",
        "url": "url",
        "description": "description",
    }

    def __init__(
        self,
        requester: RequestCallable,
        base_url: str,
        *,
        auth_token: Optional[str] = None,
        page_size: int = 50,
    ) -> None:
        self._requester = requester
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.page_size = page_size

    # -- Authentication -------------------------------------------------
    def _auth_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    # -- Networking -----------------------------------------------------
    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[MutableMapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = self._auth_headers()
        response = self._requester(method, url, params, headers)
        if not isinstance(response, dict):
            raise TypeError("Requester must return a dictionary response")
        return response

    # -- Pagination helpers --------------------------------------------
    def _pagination_params(self, page: int) -> Dict[str, Any]:
        return {"page": page, "per_page": self.page_size}

    def _extract_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = response.get(self.result_key, [])
        if not isinstance(results, list):
            raise TypeError("Response results must be provided as a list")
        return results

    def _get_next_page(
        self,
        response: Dict[str, Any],
        current_page: int,
        results_count: int,
    ) -> Optional[int]:
        if "next_page" in response:
            return response["next_page"]
        if results_count < self.page_size:
            return None
        return current_page + 1

    def _paginate(
        self,
        path: str,
        params: Optional[MutableMapping[str, Any]] = None,
    ) -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            page_params: Dict[str, Any] = dict(params or {})
            page_params.update(self._pagination_params(page))
            response = self._make_request("GET", path, page_params)
            results = self._extract_results(response)
            if not results:
                break
            for result in results:
                yield result
            next_page = self._get_next_page(response, page, len(results))
            if not next_page or next_page == page:
                break
            page = next_page

    # -- Normalisation --------------------------------------------------
    def _resolve_field(self, raw_job: Dict[str, Any], raw_field: Any) -> Any:
        if callable(raw_field):
            return raw_field(raw_job)
        if isinstance(raw_field, str) and "." in raw_field:
            value: Any = raw_job
            for part in raw_field.split("."):
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            return value
        if isinstance(raw_field, str):
            return raw_job.get(raw_field)
        return None

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        normalised: Dict[str, Any] = {}
        for target_field, raw_field in self.field_mapping.items():
            normalised[target_field] = self._resolve_field(raw_job, raw_field)
        normalised.setdefault("source", self.source_name)
        return normalised

    def fetch_normalized_jobs(self, profile: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        for raw_job in self.fetch_jobs(profile):
            yield self.normalize_job(raw_job)

    # -- Abstract API ---------------------------------------------------
    @abstractmethod
    def fetch_jobs(self, profile: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        """Yield raw job postings for the given search profile."""
        raise NotImplementedError
