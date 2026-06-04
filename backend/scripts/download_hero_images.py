"""
Download Marvel Rivals hero avatar assets from RivalSkins.

This script is intended as a one-time/local utility for collecting hero images
used by the Rivalytics frontend. It downloads named hero avatar images from the
RivalSkins hero-icons-avatars asset page and saves them into:

    frontend/public/heroes

The frontend expects filenames like:

    magneto.png
    luna-snow.png
    rocket-raccoon.png
"""

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


ASSET_INDEX_URL = "https://rivalskins.com/assets/hero-icons-avatars/"
OUTPUT_DIR = Path("frontend/public/heroes")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; RivalyticsAssetDownloader/1.0; "
        "+https://github.com/)"
    )
}


def slugify(value: str) -> str:
    """
    Convert a hero/avatar name into the frontend filename format.

    Examples:
        "luna-snow_avatar" -> "luna-snow"
        "Rocket Raccoon" -> "rocket-raccoon"
    """

    value = value.lower()
    value = value.replace("_avatar", "")
    value = re.sub(r"[^a-z0-9]+", "-", value)

    return value.strip("-")


def get_image_source(image) -> str | None:
    """
    Read an image URL from common HTML image attributes.

    Some sites use lazy-loaded image attributes instead of plain `src`, so this
    checks several possible locations.
    """

    return (
        image.get("src")
        or image.get("data-src")
        or image.get("data-lazy-src")
        or image.get("data-original")
    )


def is_named_hero_avatar(alt_text: str, image_url: str) -> bool:
    """
    Determine whether an image is a named hero avatar.

    RivalSkins also exposes generic squarehead, mask, empty, and unknown assets.
    Those are skipped because they are not clean hero-specific frontend assets.
    """

    candidate = f"{alt_text} {image_url}".lower()

    if "_avatar" not in candidate:
        return False

    ignored_tokens = [
        "img_squarehead",
        "mask_squarehead",
        "empty",
        "unknown",
    ]

    return not any(token in candidate for token in ignored_tokens)


def file_extension_from_url(url: str) -> str:
    """
    Extract the image file extension from a URL.

    Defaults to .png because the frontend recommendation cards expect PNG files.
    """

    path = urlparse(url).path
    suffix = Path(path).suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return suffix

    return ".png"


def download_file(url: str, output_path: Path) -> None:
    """
    Download a remote image file to the local filesystem.
    """

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    output_path.write_bytes(response.content)


def main() -> None:
    """
    Fetch the RivalSkins asset page, extract named hero avatars, and save them.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    response = requests.get(ASSET_INDEX_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    downloaded = 0
    skipped = 0

    for image in soup.find_all("img"):
        alt_text = image.get("alt", "").strip()
        image_src = get_image_source(image)

        if not image_src:
            skipped += 1
            continue

        image_url = urljoin(ASSET_INDEX_URL, image_src)

        if not is_named_hero_avatar(alt_text, image_url):
            skipped += 1
            continue

        raw_name = alt_text or Path(urlparse(image_url).path).stem
        hero_slug = slugify(raw_name)

        if not hero_slug:
            skipped += 1
            continue

        extension = file_extension_from_url(image_url)
        output_path = OUTPUT_DIR / f"{hero_slug}{extension}"

        download_file(image_url, output_path)
        downloaded += 1

        print(f"Downloaded {hero_slug} -> {output_path}")

    print(f"Downloaded {downloaded} hero avatars.")
    print(f"Skipped {skipped} non-hero or unsupported images.")


if __name__ == "__main__":
    main()