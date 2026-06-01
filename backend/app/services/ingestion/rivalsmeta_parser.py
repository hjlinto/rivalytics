"""
Parser utilities for converting RivalsMeta source data into ingestion schemas.

This module receives structured data extracted from RivalsMeta pages and
converts it into validated Pydantic schemas used by the ingestion pipeline.
"""

from backend.app.schemas.ingestion import HeroStatIn, TeamUpStatIn
from backend.app.services.ingestion.normalization import (
    normalize_name,
    parse_number,
    parse_percent,
)


def parse_hero_row(row: dict, season: str, source_url: str) -> HeroStatIn:
    """
    Convert a single RivalsMeta hero row into a validated hero ingestion schema.
    """

    return HeroStatIn(
        name=row["Hero"].strip(),
        normalized_name=normalize_name(row["Hero"]),
        role=row["Role"].strip(),
        tier=row.get("Tier"),
        win_rate=parse_percent(row["Win Rate"]),
        pick_rate=parse_percent(row["Pick Rate"]),
        ban_rate=parse_percent(row["Ban Rate"]),
        matches_played=parse_number(row["Matches"]),
        season=season,
        source=row.get("source", "rivalsmeta"),
        source_url=source_url,
    )


def parse_teamup_card(
    card: dict,
    season: str,
    source_url: str,
) -> list[TeamUpStatIn]:
    """
    Convert a RivalsMeta team-up card into validated team-up ingestion schemas.

    A single team-up card may contain multiple hero variants, so this function
    returns one TeamUpStatIn object per variant.
    """

    teamup_name = card["teamup_name"].strip()

    base_data = {
        "teamup_name": teamup_name,
        "normalized_teamup_name": normalize_name(teamup_name),
        "win_rate": parse_percent(card["Win Rate"]),
        "pick_rate": parse_percent(card["Pick Rate"]),
        "matches_played": parse_number(card["Matches"]),
        "season": season,
        "source": card.get("source", "rivalsmeta"),
        "source_url": source_url,
    }

    teamup_stats: list[TeamUpStatIn] = []

    for variant in card["variants"]:
        clean_heroes = [
            hero.strip()
            for hero in variant["heroes"]
            if hero.strip()
        ]

        teamup_stats.append(
            TeamUpStatIn(
                **base_data,
                heroes=clean_heroes,
                variant_size=len(clean_heroes),
            )
        )

    return teamup_stats


def parse_hero_rows(
    rows: list[dict],
    season: str,
    source_url: str,
) -> list[HeroStatIn]:
    """
    Convert multiple RivalsMeta hero rows into validated hero ingestion schemas.
    """

    return [parse_hero_row(row, season, source_url) for row in rows]


def parse_teamup_cards(
    cards: list[dict],
    season: str,
    source_url: str,
) -> list[TeamUpStatIn]:
    """
    Convert multiple RivalsMeta team-up cards into validated team-up ingestion schemas.
    """

    teamup_stats: list[TeamUpStatIn] = []

    for card in cards:
        teamup_stats.extend(parse_teamup_card(card, season, source_url))

    return teamup_stats