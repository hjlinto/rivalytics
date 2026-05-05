import requests

DEFAULT_TIMEOUT_SECONDS = 15

# We set a custom User-Agent header to identify our application when making requests to RivalsMeta.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; MarvelRivalsMetaTracker/1.0; "
        "+https://github.com/)"
    )
}

CHARACTERS_URL = "https://rivalsmeta.com/characters"
TEAMUPS_URL = "https://rivalsmeta.com/team-ups"


def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of the given URL with a timeout and error handling.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.text


def fetch_characters_html() -> str:
    """
    Fetches the HTML content for the characters page on RivalsMeta.
    """
    return fetch_html(CHARACTERS_URL)


def fetch_teamups_html() -> str:
    """
    Fetches the HTML content for the team-ups page on RivalsMeta.
    """
    return fetch_html(TEAMUPS_URL)