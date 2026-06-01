"""
Pydantic schemas for hero recommendation requests and responses.

These models define the public API contract for the recommendation endpoint.
They are intentionally kept separate from SQLAlchemy database models so the
API layer can validate request/response data without coupling directly to
database table definitions.
"""

from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    """
    Request body for generating Marvel Rivals hero recommendations.
    """

    my_team: list[str] | None = None
    enemy_team: list[str] | None = None
    bans: list[str] | None = None
    role_needed: str | None = None
    top_n: int = 5

class HeroRecommendation(BaseModel):
    """
    Single hero recommendation returned by the recommendation engine.
    """

    hero: str
    role: str
    tier: str
    score: float
    win_rate: float
    pick_rate: float
    ban_rate: float
    matches_played: int
    base_score: float
    teamup_score: float


class RecommendationResponse(BaseModel):
    """
    Response body for the recommendation endpoint.
    """

    recommendations: list[HeroRecommendation]