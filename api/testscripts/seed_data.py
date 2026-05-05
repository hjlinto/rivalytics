import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.database import Base, engine, SessionLocal
from models import Hero, TeamUp

db = SessionLocal()

"""
This script seeds the database with initial hero and teamup data for testing purposes.
"""
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
        name="Hulk",
        role="Vanguard",
        tier="A",
        win_rate=51.5,
        pick_rate=10.2,
        ban_rate=2.0,
        matches_played=14000,
        season="Season 1",
    ),
    Hero(
        name="Thor",
        role="Vanguard",
        tier="B",
        win_rate=50.2,
        pick_rate=7.1,
        ban_rate=1.5,
        matches_played=9000,
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
        name="Rocket Raccoon",
        role="Strategist",
        tier="A",
        win_rate=52.0,
        pick_rate=9.5,
        ban_rate=2.8,
        matches_played=13000,
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
    Hero(
        name="Magik",
        role="Duelist",
        tier="A",
        win_rate=52.5,
        pick_rate=8.9,
        ban_rate=3.3,
        matches_played=14000,
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
        teamup_name="Gamma Charge",
        anchor_hero="Hulk",
        partner_hero="Thor",
        win_rate=52.2,
        pick_rate=3.8,
        matches_played=6000,
        season="Season 1",
    ),
    TeamUp(
        teamup_name="Frozen Support",
        anchor_hero="Luna Snow",
        partner_hero="Rocket Raccoon",
        win_rate=53.0,
        pick_rate=4.0,
        matches_played=7000,
        season="Season 1",
    ),
    TeamUp(
        teamup_name="Shadow Combo",
        anchor_hero="Psylocke",
        partner_hero="Magik",
        win_rate=52.8,
        pick_rate=3.5,
        matches_played=6500,
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