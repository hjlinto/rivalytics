import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base, engine, SessionLocal
from models import Hero, TeamUp

db = SessionLocal()

# Hero Data
heroes = [
    Hero(
        name="Magneto",
        role="Vanguard",
        tier="A",
        win_rate=52.3,
        pick_rate=8.4,
        ban_rate=3.1,
        matches_played=12000,
        season="Season 1",
    ),
    Hero(
        name="Luna Snow",
        role="Strategist",
        tier="S",
        win_rate=54.1,
        pick_rate=12.7,
        ban_rate=5.2,
        matches_played=18000,
        season="Season 1",
    ),
    Hero(
        name="Psylocke",
        role="Duelist",
        tier="A",
        win_rate=51.8,
        pick_rate=9.2,
        ban_rate=2.4,
        matches_played=15000,
        season="Season 1",
    ),
]

for hero in heroes:
    exists = db.query(Hero).filter(Hero.name == hero.name).first()
    if not exists:
        db.add(hero)

# -------- TEAMUP DATA --------
teamups = [
    TeamUp(
        teamup_name="Magnetic Chaos",
        anchor_hero="Magneto",
        partner_hero="Scarlet Witch",
        win_rate=53.5,
        pick_rate=4.5,
        matches_played=8000,
        season="Season 1",
    ),
    TeamUp(
        teamup_name="Frozen Depths",
        anchor_hero="Luna Snow",
        partner_hero="Namor",
        win_rate=52.8,
        pick_rate=3.9,
        matches_played=6000,
        season="Season 1",
    ),
    TeamUp(
        teamup_name="Shadow Sync",
        anchor_hero="Psylocke",
        partner_hero="Magik",
        win_rate=53.1,
        pick_rate=3.2,
        matches_played=5500,
        season="Season 1",
    ),
]

for t in teamups:
    exists = (
        db.query(TeamUp)
        .filter(
            TeamUp.teamup_name == t.teamup_name,
            TeamUp.anchor_hero == t.anchor_hero,
            TeamUp.partner_hero == t.partner_hero,
        )
        .first()
    )
    if not exists:
        db.add(t)

db.commit()
db.close()

print("Seeded heroes and teamups.")