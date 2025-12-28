import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base


class Clan(Base):
    """SQLAlchemy model for the clans table."""

    __tablename__ = "clans"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String(255), nullable=False)
    region = Column(String(10), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        Index("idx_clans_name", "name"),
    )
