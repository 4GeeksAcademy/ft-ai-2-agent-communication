from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class AuthSession(SQLModel, table=True):
    """Login session row (not a SQLAlchemy DB session)."""

    __tablename__ = "auth_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked_at: Optional[datetime] = Field(default=None)
    # Area-pin hooks — unused by auth MVP; left null until area-pin feature.
    pinned_lat: Optional[float] = Field(default=None)
    pinned_lng: Optional[float] = Field(default=None)
    pinned_label: Optional[str] = Field(default=None, max_length=200)
