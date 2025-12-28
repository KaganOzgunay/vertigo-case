from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ClanCreate(BaseModel):
    """Schema for creating a new clan."""

    name: str = Field(..., min_length=1, max_length=255)
    region: str = Field(..., min_length=1, max_length=10)


class ClanResponse(BaseModel):
    """Schema for clan response."""

    id: UUID
    name: str
    region: str
    created_at: datetime

    class Config:
        from_attributes = True
