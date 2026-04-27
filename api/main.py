from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from deps import get_db
from models import Hero, TeamUp
from sqlalchemy.orm import Session
from database import engine, Base
from pydantic import BaseModel
from services.recommender import rank_heroes

Base.metadata.create_all(bind=engine)

class RecommendationRequest(BaseModel):
        my_team: list[str] | None = None
        enemy_team: list[str] | None = None
        bans: list[str] | None = None

app = FastAPI(title="Rivals Meta Tracker API", version="0.1.0")

# For local development only - will run on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint to get all heroes
@app.get("/heroes")
def get_heroes(db: Session = Depends(get_db)):
    heroes = db.query(Hero).all()

    return {
        "heroes": [
            {"id": hero.id, "name": hero.name, "role": hero.role} 
            for hero in heroes
        ]
    }

# Endpoint to get all teampups
@app.get("/teamups")
def get_teamups(db: Session = Depends(get_db)):
    teamups = db.query(TeamUp).all()
    return {
        "teamups": [
            {
                "id": teamup.id, 
                "teamup_name": teamup.teamup_name, 
                "anchor_hero": teamup.anchor_hero, 
                "partner_hero": teamup.partner_hero
            } 
            for teamup in teamups
        ]
    }

# Endpoint to get hero recommendations based on current team, enemy team, and bans
@app.post("/recommend")
def recommend_heroes(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    heroes = db.query(Hero).all()
    teamups = db.query(TeamUp).all()

    ranked = rank_heroes(
        heroes=heroes,
        teamups=teamups,
        my_team=request.my_team,
        enemy_team=request.enemy_team,
        bans=request.bans,
    )

    return {
        "recommendations": [
            {
                "hero": hero.name,
                "role": hero.role,
                "score": round(total_score, 2),
                "win_rate": hero.win_rate,
                "pick_rate": hero.pick_rate,
                "ban_rate": hero.ban_rate,
                "base_score": round(base_score, 2),
                "teamup_score": round(teamup_score, 2),
            }
            for hero, total_score, base_score, teamup_score in ranked
        ]
    }