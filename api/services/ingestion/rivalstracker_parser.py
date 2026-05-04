from api.contracts.ingestion import HeroStatIn, TeamUpStatIn
from api.services.ingestion.normalization import (
    normalize_name,
    parse_number,
    parse_percent,
)


def parse_hero_row(row: dict, season: str, source_url: str) -> HeroStatIn:
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


def parse_teamup_card(card: dict, season: str, source_url: str) -> TeamUpStatIn:
        teamup_name=card["teamup_name"].strip()

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

        results = []

        for variant in card["variants"]:
            results.append(
                TeamUpStatIn(
                    **base_data,
                    anchor_hero=variant["anchor_hero"].strip(),
                    partner_hero=variant["partner_hero"].strip(),
                )
            )
        return results

def parse_hero_rows(rows: list[dict], season: str, source_url: str) -> list[HeroStatIn]:
    return [parse_hero_row(row, season, source_url) for row in rows]


def parse_teamup_cards(cards: list[dict], season: str, source_url: str) -> list[TeamUpStatIn]:
    results = []
    for card in cards:
        results.extend(parse_teamup_card(card, season, source_url))
    return results