from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from area_todo_api.db import get_session
from area_todo_api.main import app
from area_todo_api.models import AuthSession, User  # noqa: F401

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


def _register(
    client: TestClient,
    email: str = "user@example.com",
    password: str = "password123",
):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )


def test_register_returns_token_and_user(client: TestClient) -> None:
    response = _register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 86400
    assert body["access_token"]
    assert body["user"]["email"] == "user@example.com"
    assert "password_hash" not in body["user"]


def test_register_duplicate_email_conflict(client: TestClient) -> None:
    assert _register(client).status_code == 201
    response = _register(client, email="User@example.com")

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_register_rejects_short_password(client: TestClient) -> None:
    response = _register(client, password="short")

    assert response.status_code == 422


def test_login_success_and_me(client: TestClient) -> None:
    _register(client)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    body = me.json()
    assert body["user"]["email"] == "user@example.com"
    assert body["session_id"]


def test_login_invalid_credentials(client: TestClient) -> None:
    _register(client)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_me_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_logout_revokes_session(client: TestClient) -> None:
    register = _register(client)
    token = register.json()["access_token"]

    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout.status_code == 204

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 401
