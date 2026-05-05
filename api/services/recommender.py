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

def parse_teamup_heroes(teamup: TeamUp) -> list[str]:
    """
    Extract the hero names from a teamup.
    """
    return [
        hero.strip()
        for hero in teamup.heroes.split(',')
        if hero.strip()  # filter out any empty strings
    ]

def rank_heroes(
    heroes: list[Hero],
    teamups: list[TeamUp],
    my_team: list[str] | None = None,
    enemy_team: list[str] | None = None,
    bans: list[str] | None = None,
    role_needed: str | None = None,
) -> list[tuple[Hero, float, float, float]]:
    """
    Rank heroes based on their base meta score and synergy with your current team.
    
    A teamup contributes synergy when:
    - the candidate hero is part of the teamup variant
    - at least one current ally is also part of that same variant
    """
    my_team = my_team or []
    enemy_team = enemy_team or []
    bans = bans or []
    
    # Create a set of unavailable heroes based on your team, the enemy team, and bans for quick lookup.
    unavailable_heroes = {
        name.lower()
        for name in my_team + enemy_team + bans
    }

    # Create a filtered list of heroes that excludes those on your team, the enemy team, or banned.
    filtered_heroes = [
        hero for hero in heroes 
        if hero.name.lower() not in unavailable_heroes
    ]

    # If a specific role is needed, filter heroes to only include those with that role.
    if role_needed:
        filtered_heroes = [
            hero for hero in filtered_heroes
            if hero.role.lower() == role_needed.lower()
        ]

    scored_heroes = []
    
    # For each hero, calculate their base score and then add any synergy scores from teamups with your current team.
    for hero in filtered_heroes:
        base_score = calculate_hero_score(hero)
        teamup_score_total = 0.0

        # Check each teamup to see if it includes the candidate hero and at least one ally from your current team.
        for teamup in teamups:
           teamup_heroes = parse_teamup_heroes(teamup)

           candidate_in_teamup = hero.name in teamup_heroes
           ally_in_teamup = any(ally in teamup_heroes for ally in my_team)

           if candidate_in_teamup and ally_in_teamup:
                teamup_score_total += calculate_teamup_score(teamup)

        total_score = base_score + teamup_score_total

        scored_heroes.append(
            (hero, total_score, base_score, teamup_score_total)
        )

    scored_heroes.sort(key=lambda item: item[1], reverse=True)

    return scored_heroes