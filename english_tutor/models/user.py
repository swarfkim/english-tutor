import reflex as rx
from sqlmodel import Field
from datetime import datetime
from datetime import timezone


class User(rx.Model, table=True):
    """User model for authentication and profiles."""

    username: str = Field(unique=True, index=True)
    password_hash: str
    role: str = "user"  # user, admin
    is_active: bool = True
    current_level: int = 1  # 1-8
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Session(rx.Model, table=True):
    """Chat session model."""

    user_id: int
    session_type: str = "onboarding"  # onboarding, tutoring, testing
    status: str = "active"  # active, completed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str | None = None
    is_deleted: bool = Field(default=False)
