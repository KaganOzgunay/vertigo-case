from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.clan import ClanCreate, ClanResponse
from app.services.clan_service import ClanService

router = APIRouter(prefix="/clans", tags=["clans"])


@router.post("/", response_model=ClanResponse, status_code=201)
def create_clan(clan: ClanCreate, db: Session = Depends(get_db)):
    """Create a new clan."""
    service = ClanService(db)
    return service.create(clan)


@router.get("/", response_model=List[ClanResponse])
def list_clans(db: Session = Depends(get_db)):
    """List all clans."""
    service = ClanService(db)
    return service.get_all()


@router.get("/search", response_model=List[ClanResponse])
def search_clans(
    name: str = Query(..., min_length=3, description="Search query (min 3 characters)"),
    db: Session = Depends(get_db)
):
    """Search clans by name (case-insensitive, contains match)."""
    service = ClanService(db)
    return service.search_by_name(name)


@router.delete("/{clan_id}", status_code=204)
def delete_clan(clan_id: UUID, db: Session = Depends(get_db)):
    """Delete a clan by its ID."""
    service = ClanService(db)
    if not service.delete(str(clan_id)):
        raise HTTPException(status_code=404, detail="Clan not found")
    return None
