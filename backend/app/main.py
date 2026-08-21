import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

app = FastAPI(title="JWT API")


class Credentials(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_SECONDS


def get_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT_SECRET_KEY is not configured",
        )
    return secret_key


def create_access_token(username: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=ACCESS_TOKEN_EXPIRE_SECONDS
    )
    return jwt.encode(
        {"sub": username, "exp": expires_at}, get_secret_key(), ALGORITHM
    )


def validate_token(token: str) -> str:
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not isinstance(username, str):
            raise JWTError("Missing subject")
        return username
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


@app.post("/token", response_model=TokenResponse)
def login(credentials: Credentials) -> TokenResponse:
    if (
        credentials.username != ADMIN_USERNAME
        or credentials.password != ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return TokenResponse(access_token=create_access_token(credentials.username))


@app.post("/token/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest) -> TokenResponse:
    username = validate_token(request.token)
    return TokenResponse(access_token=create_access_token(username))
