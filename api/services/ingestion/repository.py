from sqlalchemy.orm import Session

from api.models import Hero, TeamUp
from api.contracts.ingestion import HeroStatIn, TeamUpStatIn


def heroes_to_string(heroes: list[str]) -> str:
    """
    Convert a list of hero names into a comma-separated string."""
    return ",".join(hero.strip() for hero in heroes if hero.strip())


def upsert_hero(db: Session, hero: HeroStatIn) -> Hero:
    """
    Upsert a hero record based on normalized name, season, and source.
    """
    existing = (
        db.query(Hero)
        .filter(
            Hero.normalized_name == hero.normalized_name,
            Hero.season == hero.season,
            Hero.source == hero.source,
        )
        .first()
    )

    if existing is None:
        existing = Hero(
            name=hero.name,
            normalized_name=hero.normalized_name,
            role=hero.role,
            tier=hero.tier,
            win_rate=hero.win_rate,
            pick_rate=hero.pick_rate,
            ban_rate=hero.ban_rate,
            matches_played=hero.matches_played,
            season=hero.season,
            source=hero.source,
            source_url=hero.source_url,
        )
        db.add(existing)
    else:
        existing.name = hero.name
        existing.role = hero.role
        existing.tier = hero.tier
        existing.win_rate = hero.win_rate
        existing.pick_rate = hero.pick_rate
        existing.ban_rate = hero.ban_rate
        existing.matches_played = hero.matches_played
        existing.source_url = hero.source_url

    return existing


def upsert_teamup(db: Session, teamup: TeamUpStatIn) -> TeamUp:
    """
    Upsert a teamup record based on normalized teamup name, heroes, season, and source.
    """
    heroes_value = heroes_to_string(teamup.heroes)

    existing = (
        db.query(TeamUp)
        .filter(
            TeamUp.normalized_teamup_name == teamup.normalized_teamup_name,
            TeamUp.heroes == heroes_value,
            TeamUp.season == teamup.season,
            TeamUp.source == teamup.source,
        )
        .first()
    )

    if existing is None:
        existing = TeamUp(
            teamup_name=teamup.teamup_name,
            normalized_teamup_name=teamup.normalized_teamup_name,
            heroes=heroes_value,
            variant_size=teamup.variant_size,
            tier=teamup.tier,
            win_rate=teamup.win_rate,
            pick_rate=teamup.pick_rate,
            matches_played=teamup.matches_played,
            season=teamup.season,
            source=teamup.source,
            source_url=teamup.source_url,
        )
        db.add(existing)
    else:
        existing.teamup_name = teamup.teamup_name
        existing.variant_size = teamup.variant_size
        existing.tier = teamup.tier
        existing.win_rate = teamup.win_rate
        existing.pick_rate = teamup.pick_rate
        existing.matches_played = teamup.matches_played
        existing.source_url = teamup.source_url

    return existing


def upsert_heroes(db: Session, heroes: list[HeroStatIn]) -> int:
    """
    Upsert multiple hero records in a batch operation.
    """
    for hero in heroes:
        upsert_hero(db, hero)

    db.commit()
    return len(heroes)


def upsert_teamups(db: Session, teamups: list[TeamUpStatIn]) -> int:
    """
    Upsert multiple teamup records in a batch operation.
    """
    for teamup in teamups:
        upsert_teamup(db, teamup)

    db.commit()
    return len(teamups)