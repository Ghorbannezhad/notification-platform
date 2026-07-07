import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Enum as SqlEnum
from sqlmodel import Field, SQLModel


class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    FAILED = "FAILED"


class Notification(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, index=True)
    channel: str = Field(nullable=False)
    status: NotificationStatus = Field(
        sa_column=Column(
            SqlEnum(NotificationStatus, name="notification_status", native_enum=True),
            nullable=False,
            default=NotificationStatus.PENDING,
        )
    )
    payload: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
