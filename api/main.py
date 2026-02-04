from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from deps import get_db
from models import Hero
from sqlalchemy.orm import Session

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