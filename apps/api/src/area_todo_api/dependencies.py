from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from area_todo_api.db import get_session
from area_todo_api.repositories.auth_session_repository import AuthSessionRepository
from area_todo_api.repositories.todo_repository import TodoRepository
from area_todo_api.repositories.user_repository import UserRepository
from area_todo_api.security import decode_access_token
from area_todo_api.services.auth_service import AuthService, AuthenticatedPrincipal
from area_todo_api.services.todo_service import TodoService

bearer_scheme = HTTPBearer(auto_error=False)


def get_todo_repository(
    session: Session = Depends(get_session),
) -> TodoRepository:
    return TodoRepository(session)


def get_todo_service(
    repository: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(repository)


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


def get_auth_session_repository(
    session: Session = Depends(get_session),
) -> AuthSessionRepository:
    return AuthSessionRepository(session)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: AuthSessionRepository = Depends(get_auth_session_repository),
) -> AuthService:
    return AuthService(user_repository, session_repository)


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> AuthenticatedPrincipal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload["sub"])
        session_id = UUID(payload["sid"])
    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        ) from None

    return service.resolve_principal(user_id, session_id)
