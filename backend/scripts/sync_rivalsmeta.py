"""
Sync script for ingesting Marvel Rivals meta data from RivalsMeta.

This script fetches external source pages, extracts raw records, validates them
through ingestion schemas, and persists hero/team-up statistics to the database.
"""

from backend.app.db.database import SessionLocal
from backend.app.services.ingestion.rivalsmeta_client import (
    CHARACTERS_URL,
    TEAMUPS_URL,
    fetch_characters_html,
    fetch_teamups_html,
)
from backend.app.services.ingestion.rivalsmeta_parser import (
    parse_hero_rows,
    parse_teamup_cards,
)
from backend.app.services.ingestion.rivalsmeta_scraper import (
    extract_hero_rows,
    extract_teamup_cards,
)
from backend.app.services.ingestion.repository import (
    upsert_heroes,
    upsert_teamups,
)


def sync_rivalsmeta(season: str = "Current") -> None:
    """
    Fetch, parse, validate, and persist RivalsMeta data.
    """

    db = SessionLocal()

    try:
        characters_html = fetch_characters_html()
        teamups_html = fetch_teamups_html()

        hero_rows = extract_hero_rows(characters_html)
        teamup_cards = extract_teamup_cards(teamups_html)

        heroes = parse_hero_rows(
            hero_rows,
            season=season,
            source_url=CHARACTERS_URL,
        )

        teamups = parse_teamup_cards(
            teamup_cards,
            season=season,
            source_url=TEAMUPS_URL,
        )

        hero_count = upsert_heroes(db, heroes)
        teamup_count = upsert_teamups(db, teamups)

        print(f"Synced {hero_count} heroes.")
        print(f"Synced {teamup_count} team-up variants.")

    finally:
        db.close()


if __name__ == "__main__":
    sync_rivalsmeta()