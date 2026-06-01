"""
API routes for Rivalytics hero, team-up, and recommendation data.

This module owns the HTTP endpoints that expose Marvel Rivals meta data to the
frontend.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.deps import get_db
from backend.app.models import Hero, TeamUp
from backend.app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from backend.app.services.recommender import rank_heroes


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """
    Health check endpoint used to confirm the API is running.
    """

    return {"status": "ok"}


@router.get("/heroes")
def get_heroes(db: Session = Depends(get_db)) -> dict:
    """
    Return all heroes stored in the database.
    """

    heroes = db.query(Hero).all()

    return {
        "heroes": [
            {
                "id": hero.id,
                "name": hero.name,
                "role": hero.role,
            }
            for hero in heroes
        ]
    }


@router.get("/teamups")
def get_teamups(db: Session = Depends(get_db)) -> dict:
    """
    Return all team-up combinations stored in the database.
    """

    teamups = db.query(TeamUp).all()

    return {
        "teamups": [
            {
                "id": teamup.id,
                "teamup_name": teamup.teamup_name,
                "heroes": teamup.heroes.split(","),
                "variant_size": teamup.variant_size,
                "tier": teamup.tier,
                "win_rate": teamup.win_rate,
                "pick_rate": teamup.pick_rate,
                "matches_played": teamup.matches_played,
            }
            for teamup in teamups
        ]
    }


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_heroes(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Recommend heroes based on team context, enemy picks, bans, role needs, and meta data.
    """

    heroes = db.query(Hero).all()
    teamups = db.query(TeamUp).all()

    ranked = rank_heroes(
        heroes=heroes,
        teamups=teamups,
        my_team=request.my_team,
        enemy_team=request.enemy_team,
        bans=request.bans,
        role_needed=request.role_needed,
    )

    top_recommendations = ranked[: request.top_n]

    return {
        "recommendations": [
            {
                "hero": hero.name,
                "role": hero.role,
                "tier": hero.tier,
                "score": round(total_score, 2),
                "win_rate": hero.win_rate,
                "pick_rate": hero.pick_rate,
                "ban_rate": hero.ban_rate,
                "matches_played": hero.matches_played,
                "base_score": round(base_score, 2),
                "teamup_score": round(teamup_score, 2),
            }
            for hero, total_score, base_score, teamup_score in top_recommendations
        ]
    }