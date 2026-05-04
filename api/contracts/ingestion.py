from datetime import datetime, timezone
from pydantic import BaseModel, Field

# Pydantic models for data ingestion
class HeroStatIn(BaseModel):
    name: str
    normalized_name: str
    role: str
    tier: str | None = None

    win_rate: float
    pick_rate: float
    ban_rate: float
    matches_played: int
    season: str
    game_mode: str = "competitive"

    source: str = "rivalstracker"
    source_url: str
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Pydantic model for teamup stats ingestion
class TeamUpStatIn(BaseModel):
    teamup_name: str
    normalized_teamup_name: str
    heroes: list[str]
    variant_size: int

    win_rate: float
    pick_rate: float | None = None
    matches_played: int
    season: str
    game_mode: str = "competitive"

    source: str = "rivalstracker"
    source_url: str
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

