from __future__ import annotations

from backend.ingest.greenhouse import GreenhouseJobSourceClient


def test_greenhouse_query_construction(requester_factory, profile):
    requester = requester_factory([
        {"results": []},
    ])
    client = GreenhouseJobSourceClient(
        requester=requester,
        base_url="https://api.greenhouse.io",
        auth_token=None,
        page_size=50,
    )

    list(client.fetch_jobs(profile))

    assert len(requester.calls) == 1
    call = requester.calls[0]
    assert call.url == "https://api.greenhouse.io/greenhouse/jobs"
    assert call.params["query"] == "python backend"
    assert call.params["levels"] == "senior"
    assert call.params["departments"] == "saas,fintech"
    assert "Authorization" not in call.headers


def test_greenhouse_pagination(requester_factory, profile):
    requester = requester_factory(
        [
            {"results": [{"id": 1}, {"id": 2}], "next_page": 3},
            {"results": [{"id": 3}], "next_page": None},
        ]
    )
    client = GreenhouseJobSourceClient(
        requester=requester,
        base_url="https://api.greenhouse.io",
        page_size=2,
    )

    jobs = list(client.fetch_jobs(profile))

    assert [job["id"] for job in jobs] == [1, 2, 3]
    assert [call.params["page"] for call in requester.calls] == [1, 3]


def test_greenhouse_normalisation(requester_factory, profile):
    requester = requester_factory(
        [
            {
                "results": [
                    {
                        "id": 321,
                        "title": "Staff Data Scientist",
                        "metadata": {"company": "DataCorp"},
                        "location": {"name": "New York"},
                        "absolute_url": "https://boards.greenhouse.io/datacorp/jobs/321",
                        "content": "Greenhouse job description",
                    }
                ]
            }
        ]
    )
    client = GreenhouseJobSourceClient(
        requester=requester,
        base_url="https://api.greenhouse.io",
    )

    jobs = list(client.fetch_normalized_jobs(profile))

    assert jobs == [
        {
            "id": 321,
            "title": "Staff Data Scientist",
            "company_name": "DataCorp",
            "location": "New York",
            "url": "https://boards.greenhouse.io/datacorp/jobs/321",
            "description": "Greenhouse job description",
            "source": "greenhouse",
        }
    ]
