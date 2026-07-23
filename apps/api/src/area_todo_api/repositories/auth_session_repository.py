from datetime import datetime
from uuid import UUID

from sqlmodel import Session

from area_todo_api.models.auth_session import AuthSession


class AuthSessionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, session_id: UUID) -> AuthSession | None:
        return self.session.get(AuthSession, session_id)

    def create(self, auth_session: AuthSession) -> AuthSession:
        self.session.add(auth_session)
        self.session.commit()
        self.session.refresh(auth_session)
        return auth_session

    def revoke(self, auth_session: AuthSession, revoked_at: datetime) -> AuthSession:
        auth_session.revoked_at = revoked_at
        self.session.add(auth_session)
        self.session.commit()
        self.session.refresh(auth_session)
        return auth_session
