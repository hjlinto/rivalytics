import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Hero, TeamUp
from services.recommender import rank_heroes


def main():
    """
    Test the hero recommendation system by ranking heroes based on a sample team composition.
    This function sets up a sample team and enemy composition, retrieves hero and teamup data from the database,
    and prints out the ranked heroes with their scores.
    """
    db = SessionLocal()

    my_team = ["Scarlet Witch"]
    enemy_team = ["Luna Snow"]
    bans = ["Psylocke"]

    heroes = db.query(Hero).all()
    teamups = db.query(TeamUp).all()

    ranked_heroes = rank_heroes(
        heroes=heroes,
        teamups=teamups,
        my_team=my_team,
        enemy_team=enemy_team,
        bans=bans,
    )

    print(f"Hero rankings for team: {my_team}")

    for hero, total_score, base_score, teamup_score in ranked_heroes:
        print(
            f"{hero.name} | role={hero.role} | "
            f"base={base_score:.2f} | "
            f"teamup={teamup_score:.2f} | "
            f"total={total_score:.2f}"
        )
    db.close()


if __name__ == "__main__":
    main()