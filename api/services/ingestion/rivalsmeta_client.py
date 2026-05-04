import requests

DEFAULT_TIMEOUT_SECONDS = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; MarvelRivalsMetaTracker/1.0; "
        "+https://github.com/)"
    )
}

CHARACTERS_URL = "https://rivalsmeta.com/characters"
TEAMUPS_URL = "https://rivalsmeta.com/team-ups"


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.text


def fetch_characters_html() -> str:
    return fetch_html(CHARACTERS_URL)


def fetch_teamups_html() -> str:
    return fetch_html(TEAMUPS_URL)