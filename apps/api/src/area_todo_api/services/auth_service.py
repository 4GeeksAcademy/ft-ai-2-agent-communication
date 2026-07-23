from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status

from area_todo_api.config import settings
from area_todo_api.models.auth_session import AuthSession
from area_todo_api.models.user import User
from area_todo_api.repositories.auth_session_repository import AuthSessionRepository
from area_todo_api.repositories.user_repository import UserRepository
from area_todo_api.schemas.auth import (
    AuthCredentials,
    MeResponse,
    TokenResponse,
    UserRead,
)
from area_todo_api.security import (
    create_access_token,
    hash_password,
    verify_password,
)


@dataclass
class AuthenticatedPrincipal:
    user: User
    session: AuthSession


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: AuthSessionRepository,
    ) -> None:
        self.user_repository = user_repository
        self.session_repository = session_repository

    def register(self, credentials: AuthCredentials) -> TokenResponse:
        email = credentials.email.lower()
        if self.user_repository.get_by_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            email=email,
            password_hash=hash_password(credentials.password),
        )
        created_user = self.user_repository.create(user)
        return self._issue_token(created_user)

    def login(self, credentials: AuthCredentials) -> TokenResponse:
        email = credentials.email.lower()
        user = self.user_repository.get_by_email(email)
        if user is None or not verify_password(
            user.password_hash, credentials.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        return self._issue_token(user)

    def logout(self, principal: AuthenticatedPrincipal) -> None:
        self.session_repository.revoke(principal.session, datetime.utcnow())

    def me(self, principal: AuthenticatedPrincipal) -> MeResponse:
        return MeResponse(
            user=UserRead.model_validate(principal.user),
            session_id=principal.session.id,
        )

    def resolve_principal(
        self, user_id: UUID, session_id: UUID
    ) -> AuthenticatedPrincipal:
        auth_session = self.session_repository.get_by_id(session_id)
        if auth_session is None or not self._is_session_valid(auth_session):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        if auth_session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        return AuthenticatedPrincipal(user=user, session=auth_session)

    def _issue_token(self, user: User) -> TokenResponse:
        expires_at = datetime.utcnow() + timedelta(
            seconds=settings.jwt_expires_seconds
        )
        auth_session = self.session_repository.create(
            AuthSession(user_id=user.id, expires_at=expires_at)
        )
        access_token, _ = create_access_token(
            user_id=user.id,
            session_id=auth_session.id,
            expires_at=expires_at,
        )
        return TokenResponse(
            access_token=access_token,
            expires_in=settings.jwt_expires_seconds,
            user=UserRead.model_validate(user),
        )

    @staticmethod
    def _is_session_valid(auth_session: AuthSession) -> bool:
        if auth_session.revoked_at is not None:
            return False
        return auth_session.expires_at > datetime.utcnow()
