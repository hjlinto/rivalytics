import re

def normalize_name(name: str) -> str:
    """
    Normalize hero/teamup names for consistent matching.
    """
    # Convert to lowercase
    normalized = name.lower()
    
    # Remove non-alphanumeric characters
    normalized = re.sub(r'[^a-z0-9]', '', normalized)
    
    return normalized

def parse_percent(value: str | float | None) -> float | None:
    """
    Parse a percentage string (e.g., "50%") into a float (e.g., 0.5).
    """
    if value is None:
        return None
    
    if isinstance(value, float):
        return value
    
    value = value.strip().replace('%', '')
    return float(value) if value else None

def parse_number(value: str | float | None) -> int | None:
    """
    Parse a number string (e.g., "1,000") into an integer (e.g., 1000).
    """
    if value is None:
        return None
    
    if isinstance(value, int):
        return value
    
    value = value.replace(',', '').strip()
    return int(value) if value else None