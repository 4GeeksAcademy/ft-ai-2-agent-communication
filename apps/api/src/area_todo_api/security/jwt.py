from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt

from area_todo_api.config import settings


def create_access_token(
    *,
    user_id: UUID,
    session_id: UUID,
    expires_at: datetime | None = None,
) -> tuple[str, datetime]:
    if expires_at is None:
        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=settings.jwt_expires_seconds
        )
    elif expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    payload = {
        "sub": str(user_id),
        "sid": str(session_id),
        "exp": expires_at,
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token, expires_at.replace(tzinfo=None)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
