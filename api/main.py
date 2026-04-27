from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from deps import get_db
from models import Hero, TeamUp
from sqlalchemy.orm import Session
from database import engine, Base

Base.metadata.create_all(bind=engine)

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