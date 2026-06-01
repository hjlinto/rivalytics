"""
Recommendation scoring service for Rivalytics.

This module owns the core hero-ranking logic. It combines individual hero meta
statistics with team-up synergy signals to produce ranked Marvel Rivals hero
recommendations for the API layer.
"""

from backend.app.models import Hero, TeamUp


def calculate_hero_score(hero: Hero) -> float:
    """
    Calculate a hero's base meta score.

    The current scoring formula treats win rate, pick rate, and ban rate as
    positive signals:

    - win_rate: the hero is performing well.
    - pick_rate: the hero is commonly trusted by players.
    - ban_rate: the hero is strong enough to draw bans.
    """

    return (
        hero.win_rate * 0.60
        + hero.pick_rate * 0.20
        + hero.ban_rate * 0.20
    )


def calculate_teamup_score(teamup: TeamUp) -> float:
    """
    Calculate a team-up synergy score.

    Win rate and pick rate are treated as positive team-up signals.
    """

    pick_rate = teamup.pick_rate or 0.0

    return teamup.win_rate * 0.70 + pick_rate * 0.30


def parse_teamup_heroes(teamup: TeamUp) -> list[str]:
    """
    Parse the participating heroes from a team-up record.
    """

    return [
        hero.strip()
        for hero in teamup.heroes.split(",")
        if hero.strip()
    ]


def normalize_names(names: list[str] | None) -> set[str]:
    """
    Normalize a list of hero names for case-insensitive comparison.
    """

    return {name.lower() for name in names or []}


def rank_heroes(
    heroes: list[Hero],
    teamups: list[TeamUp],
    my_team: list[str] | None = None,
    enemy_team: list[str] | None = None,
    bans: list[str] | None = None,
    role_needed: str | None = None,
) -> list[tuple[Hero, float, float, float]]:
    """
    Rank heroes using meta strength and team-up synergy.

    Heroes are filtered according to Marvel Rivals draft rules:

    - Heroes already selected by allies are unavailable.
    - Banned heroes are unavailable.
    - Optional role filtering can be applied.

    Team-up synergy is awarded when:
    - The candidate hero participates in a team-up variant.
    - At least one ally already selected is also part of that variant.
    """

    my_team_names = normalize_names(my_team)
    enemy_team_names = normalize_names(enemy_team)
    banned_names = normalize_names(bans)

    unavailable_heroes = my_team_names | banned_names

    filtered_heroes = [
        hero
        for hero in heroes
        if hero.name.lower() not in unavailable_heroes
    ]

    if role_needed:
        filtered_heroes = [
            hero
            for hero in filtered_heroes
            if hero.role.lower() == role_needed.lower()
        ]

    scored_heroes: list[tuple[Hero, float, float, float]] = []

    for hero in filtered_heroes:
        base_score = calculate_hero_score(hero)
        teamup_score_total = 0.0

        candidate_name = hero.name.lower()

        for teamup in teamups:
            teamup_heroes = normalize_names(
                parse_teamup_heroes(teamup)
            )

            candidate_in_teamup = candidate_name in teamup_heroes
            ally_in_teamup = bool(my_team_names & teamup_heroes)

            if candidate_in_teamup and ally_in_teamup:
                teamup_score_total += calculate_teamup_score(teamup)

        total_score = base_score + teamup_score_total

        scored_heroes.append(
            (
                hero,
                total_score,
                base_score,
                teamup_score_total,
            )
        )

    scored_heroes.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return scored_heroes