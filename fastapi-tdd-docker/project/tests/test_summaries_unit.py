import json
from datetime import datetime
from app.api import summaries

import pytest

from app.api import crud, summaries


def test_create_summary(test_app_with_db, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return None
    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar/"


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.10/v/missing",
            }
        ]
    }

    response = test_app.post("/summaries/", data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": "http://testdriven.io",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "http://testdriven.io/",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        }
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "http://testdriven.io/",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io/",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        }
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": "http://testdriven.io",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "http://testdriven.io/"}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {"url": "http://testdriven.io/", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "url": "http://testdriven.io/",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/summaries/1/", data=json.dumps(test_request_payload),)
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "http://testdriven.io/", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "http://testdriven.io/", "summary": "updated!"},
            422,
            [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0},
                    "url": "https://errors.pydantic.dev/2.10/v/greater_than",
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "url"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
                },
            ],
        ],
        [
            1,
            {"url": "http://testdriven.io/"},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {"url": "http://testdriven.io/"},
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(test_app, monkeypatch, summary_id, payload, status_code, detail):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail