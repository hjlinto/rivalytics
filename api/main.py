from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rivals Meta Tracker API", version="0.1.0")

# For local development only - will run on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary hardcoded hero list - to be replaced with database integration
heroes = [
    {"id": 1, "name": "Peni Parker", "role": "Vanguard"},
    {"id": 2, "name": "Psylocke", "role": "Duelist"},
    {"id": 3, "name": "Invisible Woman", "role": "Strategist"},
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/heroes")
def get_heroes():
    return {"heroes": heroes}