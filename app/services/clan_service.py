from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.clan import Clan
from app.schemas.clan import ClanCreate


class ClanService:
    """Service layer for clan business logic."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, clan_data: ClanCreate) -> Clan:
        """Create a new clan."""
        clan = Clan(
            name=clan_data.name,
            region=clan_data.region
        )
        self.db.add(clan)
        self.db.commit()
        self.db.refresh(clan)
        return clan

    def get_all(self) -> List[Clan]:
        """Get all clans."""
        return self.db.query(Clan).all()

    def search_by_name(self, name: str) -> List[Clan]:
        """Search clans by name (case-insensitive, contains)."""
        return self.db.query(Clan).filter(
            Clan.name.ilike(f"%{name}%")
        ).all()

    def get_by_id(self, clan_id: str) -> Optional[Clan]:
        """Get a clan by its ID."""
        return self.db.query(Clan).filter(Clan.id == clan_id).first()

    def delete(self, clan_id: str) -> bool:
        """Delete a clan by its ID. Returns True if deleted, False if not found."""
        clan = self.get_by_id(clan_id)
        if clan:
            self.db.delete(clan)
            self.db.commit()
            return True
        return False
