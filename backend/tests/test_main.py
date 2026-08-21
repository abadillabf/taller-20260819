import os
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

from app.main import ALGORITHM, app

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
client = TestClient(app)


def test_login_returns_a_jwt_with_five_minute_expiration() -> None:
    before = datetime.now(timezone.utc)

    response = client.post("/token", json={"username": "admin", "password": "admin123"})

    assert response.status_code == 200
    body = response.json()
    payload = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "admin"
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 300
    assert 299 <= payload["exp"] - before.timestamp() <= 301


def test_login_rejects_invalid_credentials() -> None:
    response = client.post("/token", json={"username": "admin", "password": "wrong"})

    assert response.status_code == 401


def test_refresh_returns_a_new_token_for_a_valid_token() -> None:
    token = client.post(
        "/token", json={"username": "admin", "password": "admin123"}
    ).json()["access_token"]

    response = client.post("/token/refresh", json={"token": token})

    assert response.status_code == 200
    assert jwt.decode(
        response.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM]
    )["sub"] == "admin"


def test_refresh_rejects_an_expired_token() -> None:
    expired_token = jwt.encode(
        {"sub": "admin", "exp": datetime.now(timezone.utc) - timedelta(seconds=1)},
        SECRET_KEY,
        ALGORITHM,
    )

    response = client.post("/token/refresh", json={"token": expired_token})

    assert response.status_code == 401
