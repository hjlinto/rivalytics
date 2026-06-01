"""
HTTP client for retrieving Marvel Rivals meta data from RivalsMeta.

This module is responsible only for network communication. Parsing,
normalization, and database persistence are handled elsewhere in the ingestion
pipeline.
"""

import requests


DEFAULT_TIMEOUT_SECONDS = 15

RIVALSMETA_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; Rivalytics/1.0; "
        "+https://github.com/)"
    )
}

CHARACTERS_URL = "https://rivalsmeta.com/characters"
TEAMUPS_URL = "https://rivalsmeta.com/team-ups"


def fetch_html(url: str) -> str:
    """
    Retrieve raw HTML from a RivalsMeta page.
    """

    response = requests.get(
        url,
        headers=RIVALSMETA_HEADERS,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    return response.text


def fetch_characters_html() -> str:
    """
    Retrieve the RivalsMeta character statistics page.
    """

    return fetch_html(CHARACTERS_URL)


def fetch_teamups_html() -> str:
    """
    Retrieve the RivalsMeta team-up statistics page.
    """

    return fetch_html(TEAMUPS_URL)