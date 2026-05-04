from bs4 import BeautifulSoup


def role_from_src(src: str) -> str:
    src = src.lower()

    if "vanguard" in src:
        return "Vanguard"
    if "duelist" in src:
        return "Duelist"
    if "strategist" in src:
        return "Strategist"

    return "Unknown"


def extract_hero_rows(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    for tr in soup.find_all("tr"):
        hero_link = tr.select_one("a.cha")
        if hero_link is None:
            continue

        name_el = hero_link.select_one(".name")
        role_img = tr.select_one("img.hero-class")
        tier_el = tr.select_one(".tier")

        cells = tr.find_all("td")

        if not name_el or not role_img or not tier_el or len(cells) < 7:
            continue

        rows.append(
            {
                "Hero": name_el.get_text(strip=True),
                "Role": role_from_src(role_img.get("src", "")),
                "Tier": tier_el.get_text(strip=True),
                "Win Rate": cells[3].get_text(strip=True),
                "Pick Rate": cells[4].get_text(strip=True),
                "Ban Rate": cells[5].get_text(strip=True),
                "Matches": cells[6].get_text(strip=True),
            }
        )

    return rows

def extract_teamup_cards(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    cards = []

    for article in soup.select("article.teamup-card"):
        name_el = article.select_one(".card-head .name")
        tier_el = article.select_one(".tier-letter")
        win_rate_el = article.select_one(".card-stats .wr")
        pick_rate_el = article.select_one(".card-stats .pr")

        stat_values = article.select(".card-stats .val")
        matches_el = stat_values[2] if len(stat_values) >= 3 else None

        if not name_el or not tier_el or not win_rate_el or not pick_rate_el or not matches_el:
            continue

        variants = []

        for variant_row in article.select(".variant-row"):
            hero_imgs = variant_row.select(".v-hero img")

            hero_names = [
                img.get("alt", "").strip()
                for img in hero_imgs
                if img.get("alt", "").strip()
            ]

            if len(hero_names) < 2:
                continue

            variants.append(
                {
                    "heroes": hero_names,
                }
            )

        cards.append(
            {
                "teamup_name": name_el.get_text(strip=True),
                "Tier": tier_el.get_text(strip=True),
                "Win Rate": win_rate_el.get_text(strip=True),
                "Pick Rate": pick_rate_el.get_text(strip=True),
                "Matches": matches_el.get_text(strip=True),
                "variants": variants,
            }
        )

    return cards