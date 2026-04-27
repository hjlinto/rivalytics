from models import Hero, TeamUp


def calculate_hero_score(hero: Hero) -> float:
    """
    Calculate a base meta score for a hero.

    Win rate, pick rate, and ban rate are all treated as positive signals:
    - win_rate: hero is performing well
    - pick_rate: hero is commonly trusted/played
    - ban_rate: hero is likely strong enough to be targeted by bans
    """
    score = 0.0

    score += hero.win_rate * 0.60
    score += hero.pick_rate * 0.20
    score += hero.ban_rate * 0.20

    return score

def calculate_teamup_score(teamup: TeamUp) -> float:
    """
    Calculate a synergy score for a teamup.

    Win rate and pick rate are treated as positive signals:
    - win_rate: teamup is performing well
    - pick_rate: teamup is commonly trusted/played
    """
    score = 0.0

    score += teamup.win_rate * 0.70
    score += teamup.pick_rate * 0.30

    return score

def rank_heroes(
    heroes: list[Hero],
    teamups: list[TeamUp],
    my_team: list[str] | None = None,
    enemy_team: list[str] | None = None,
    bans: list[str] | None = None,
) -> list[tuple[Hero, float, float, float]]:
    """
    Rank heroes by base meta score + teamup synergy with current team.

    Returns:
        (hero, total_score, base_score, teamup_score)
    """
    my_team = my_team or []
    enemy_team = enemy_team or []
    bans = bans or []

    unavailable_heroes = set(my_team + enemy_team + bans)
    
    filtered_heroes = [hero for hero in heroes if hero.name not in unavailable_heroes]

    scored_heroes = []

    for hero in filtered_heroes:
        base_score = calculate_hero_score(hero)
        teamup_score_total = 0.0

        # check if this hero has a teamup with anyone on your team
        for teamup in teamups:
            is_anchor_match = (
                teamup.anchor_hero == hero.name
                and teamup.partner_hero in my_team
            )

            is_partner_match = (
                teamup.partner_hero == hero.name
                and teamup.anchor_hero in my_team
            )

            if is_anchor_match or is_partner_match:
                teamup_score_total += calculate_teamup_score(teamup)

        total_score = base_score + teamup_score_total

        scored_heroes.append(
            (hero, total_score, base_score, teamup_score_total)
        )

    scored_heroes.sort(key=lambda item: item[1], reverse=True)

    return scored_heroes