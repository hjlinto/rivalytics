from api.database import SessionLocal
from api.services.ingestion.rivalsmeta_client import (
    CHARACTERS_URL,
    TEAMUPS_URL,
    fetch_characters_html,
    fetch_teamups_html,
)
from api.services.ingestion.rivalsmeta_scraper import (
    extract_hero_rows,
    extract_teamup_cards,
)
from api.services.ingestion.rivalsmeta_parser import (
    parse_hero_rows,
    parse_teamup_cards,
)
from api.services.ingestion.repository import (
    upsert_heroes,
    upsert_teamups,
)


def sync_rivalsmeta(season: str = "Current") -> None:
    """
    Fetch RivalsMeta data, parse it, and save it to the database.
    """
    db = SessionLocal()

    # Fetch and parse data, then upsert into the database
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

        print(f"Synced {hero_count} heroes")
        print(f"Synced {teamup_count} teamup variants")

    finally:
        db.close()

# Run the sync function if this script is executed directly
if __name__ == "__main__":
    sync_rivalsmeta()