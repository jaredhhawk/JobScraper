from __future__ import annotations

import pathlib
import sys

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@dataclass
class RequestCall:
    method: str
    url: str
    params: Dict[str, Any]
    headers: Dict[str, str]


class RequestStub:
    """Simple stub that records requests and yields predetermined responses."""

    def __init__(self, responses: Iterable[Dict[str, Any]]) -> None:
        self._responses: List[Dict[str, Any]] = list(responses)
        self.calls: List[RequestCall] = []

    def __call__(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        if not self._responses:
            raise AssertionError("No stub response available for request")
        call = RequestCall(method, url, params or {}, headers or {})
        self.calls.append(call)
        return self._responses.pop(0)


@pytest.fixture
def profile() -> Dict[str, Any]:
    return {
        "role_keywords": ["python", "backend"],
        "seniority": ["senior"],
        "industries": ["saas", "fintech"],
    }


@pytest.fixture
def requester_factory():
    def factory(responses: Iterable[Dict[str, Any]]) -> RequestStub:
        return RequestStub(responses)

    return factory
