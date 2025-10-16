from __future__ import annotations

from backend.ingest.builtin import BuiltinJobSourceClient


def test_builtin_query_construction(requester_factory, profile):
    requester = requester_factory([
        {"results": []},
    ])
    client = BuiltinJobSourceClient(
        requester=requester,
        base_url="https://api.example.com",
        auth_token="secret",
        page_size=25,
    )

    list(client.fetch_jobs(profile))

    assert len(requester.calls) == 1
    call = requester.calls[0]
    assert call.method == "GET"
    assert call.url == "https://api.example.com/jobs"
    assert call.params["keywords"] == "python,backend"
    assert call.params["seniority"] == "senior"
    assert call.params["industries"] == "saas,fintech"
    assert call.headers["Authorization"] == "Bearer secret"


def test_builtin_pagination(requester_factory, profile):
    requester = requester_factory(
        [
            {"results": [{"id": "1"}, {"id": "2"}]},
            {"results": [{"id": "3"}]},
        ]
    )
    client = BuiltinJobSourceClient(
        requester=requester,
        base_url="https://api.example.com",
        page_size=2,
    )

    jobs = list(client.fetch_jobs(profile))

    assert [job["id"] for job in jobs] == ["1", "2", "3"]
    assert len(requester.calls) == 2
    assert requester.calls[0].params["page"] == 1
    assert requester.calls[1].params["page"] == 2


def test_builtin_normalisation(requester_factory, profile):
    requester = requester_factory(
        [
            {
                "results": [
                    {
                        "id": "abc",
                        "title": "Senior Backend Engineer",
                        "company": "Acme",
                        "location": "Remote",
                        "apply_link": "https://example.com/jobs/abc",
                        "description": "Job description",
                    }
                ]
            }
        ]
    )
    client = BuiltinJobSourceClient(
        requester=requester,
        base_url="https://api.example.com",
    )

    jobs = list(client.fetch_normalized_jobs(profile))

    assert jobs == [
        {
            "id": "abc",
            "title": "Senior Backend Engineer",
            "company_name": "Acme",
            "location": "Remote",
            "url": "https://example.com/jobs/abc",
            "description": "Job description",
            "source": "builtin",
        }
    ]
