import sys
from types import ModuleType, SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDENT_DATABASE_PATH", str(tmp_path / "test_students.db"))
    with TestClient(app) as test_client:
        yield test_client


def student_payload(**overrides):
    payload = {
        "name": "Asha Patel",
        "date_of_birth": "2006-04-15",
        "email": "asha@example.com",
        "phone": "555-0101",
        "course": "Python Backend",
        "address": "12 Example Road",
        "enrollment_date": "2025-09-01",
    }
    payload.update(overrides)
    return payload


def test_student_crud_flow(client):
    created = client.post("/students", json=student_payload())
    assert created.status_code == 201
    student = created.json()
    student_id = student["student_id"]
    assert student["name"] == "Asha Patel"

    fetched = client.get(f"/students/{student_id}")
    assert fetched.status_code == 200
    assert fetched.json() == student

    updated = client.patch(
        f"/students/{student_id}", json={"course": "Data Science"}
    )
    assert updated.status_code == 200
    assert updated.json()["course"] == "Data Science"

    listed = client.get("/students", params={"course": "data science"})
    assert listed.status_code == 200
    assert [item["student_id"] for item in listed.json()] == [student_id]

    deleted = client.delete(f"/students/{student_id}")
    assert deleted.status_code == 204
    assert client.get(f"/students/{student_id}").status_code == 404


def test_student_records_persist_between_requests(client):
    client.post("/students", json=student_payload())

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "payload",
    [
        student_payload(email=None, phone=None),
        student_payload(email="not-an-email"),
        student_payload(date_of_birth="not-a-date"),
    ],
)
def test_invalid_student_data_is_rejected(client, payload):
    response = client.post("/students", json=payload)

    assert response.status_code == 422


def test_update_cannot_remove_all_contact_information(client):
    created = client.post("/students", json=student_payload(phone=None))

    response = client.patch(
        f"/students/{created.json()['student_id']}", json={"email": None}
    )

    assert response.status_code == 422


def test_missing_student_returns_not_found(client):
    assert client.get("/students/999").status_code == 404
    assert client.patch("/students/999", json={"course": "Math"}).status_code == 404
    assert client.delete("/students/999").status_code == 404


def test_ai_query_uses_student_records_without_contact_details(client, monkeypatch):
    client.post("/students", json=student_payload())
    captured = {}

    class FakeChatOllama:
        def __init__(self, **options):
            captured["options"] = options

        def invoke(self, prompt):
            captured["prompt"] = prompt
            return SimpleNamespace(content="There is one student.")

    fake_module = ModuleType("langchain_ollama")
    fake_module.ChatOllama = FakeChatOllama
    monkeypatch.setitem(sys.modules, "langchain_ollama", fake_module)

    response = client.post(
        "/ai/query-students", json={"question": "How many students are there?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "There is one student."
    assert "Asha Patel" in captured["prompt"]
    assert "asha@example.com" not in captured["prompt"]
    assert captured["options"]["model"] == "llama3.2:1b"