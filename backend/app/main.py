import hmac
import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
app = FastAPI(title="JWT API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


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


def valid_credentials(credentials: Credentials) -> bool:
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin credentials are not configured",
        )
    return hmac.compare_digest(credentials.username, username) and hmac.compare_digest(
        credentials.password, password
    )


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
    if not valid_credentials(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return TokenResponse(access_token=create_access_token(credentials.username))


@app.post("/token/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest) -> TokenResponse:
    username = validate_token(request.token)
    return TokenResponse(access_token=create_access_token(username))
