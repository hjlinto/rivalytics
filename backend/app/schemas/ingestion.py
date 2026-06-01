"""
Pydantic schemas for ingesting Marvel Rivals meta statistics.

These schemas define the validated shape of external source data after parsing
and normalization, but before it is persisted into SQLAlchemy database models.
"""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class HeroStatIn(BaseModel):
    """
    Validated hero statistics produced by the ingestion pipeline.
    """

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


class TeamUpStatIn(BaseModel):
    """
    Validated team-up statistics produced by the ingestion pipeline.
    """

    teamup_name: str
    normalized_teamup_name: str
    heroes: list[str]
    variant_size: int

    win_rate: float
    pick_rate: float | None = None
    matches_played: int

    season: str
    game_mode: str = "competitive"
    tier: str | None = None
    source: str = "rivalstracker"
    source_url: str
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))