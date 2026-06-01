"""
Normalization utilities for the Rivalytics ingestion pipeline.

These functions transform raw source values into consistent application-level
formats before validation and persistence.
"""

import re


def normalize_name(name: str) -> str:
    """
    Normalize hero and team-up names for consistent matching.

    Normalization rules:
    - Convert to lowercase.
    - Remove whitespace.
    - Remove punctuation and special characters.
    """

    normalized = name.lower()
    normalized = re.sub(r"[^a-z0-9]", "", normalized)

    return normalized


def parse_percent(value: str | float | int | None) -> float | None:
    """
    Convert a percentage value into a numeric float.
    """

    if value is None:
        return None

    if isinstance(value, (float, int)):
        return float(value)

    value = value.strip().replace("%", "")

    return float(value) if value else None


def parse_number(value: str | int | None) -> int | None:
    """
    Convert a formatted numeric string into an integer.
    """

    if value is None:
        return None

    if isinstance(value, int):
        return value

    value = value.replace(",", "").strip()

    return int(value) if value else None