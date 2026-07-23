from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from area_todo_api.db import get_session
from area_todo_api.main import app
from area_todo_api.models import AuthSession, Todo, User  # noqa: F401

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    def get_test_session() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_todos_empty(client: TestClient) -> None:
    response = client.get("/api/v1/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_list_todo(client: TestClient) -> None:
    payload = {
        "title": "Buy milk",
        "description": "At the corner store",
        "latitude": 43.6532,
        "longitude": -79.3832,
    }

    create_response = client.post("/api/v1/todos", json=payload)
    assert create_response.status_code == 201

    created = create_response.json()
    assert created["title"] == payload["title"]
    assert created["latitude"] == payload["latitude"]
    assert created["completed"] is False

    list_response = client.get("/api/v1/todos")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
