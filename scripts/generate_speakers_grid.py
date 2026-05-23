#!/usr/bin/env python3
"""
Generate the speakers grid in speakers.html from data/speakers.json.

Usage:
    cd /path/to/capetown-2027
    python3 scripts/generate_speakers_grid.py

Reads:
    data/speakers.json   — speaker data
    speakers.html        — page with placeholder collection item

Writes:
    speakers.html        — updated with full speaker grid
"""

import json
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEAKERS_JSON = REPO_ROOT / "data" / "speakers.json"
SPEAKERS_HTML = REPO_ROOT / "speakers.html"

# Markers: we find the speakers-collection div and replace its contents
COLLECTION_OPEN = '<div class="speakers-collection">'
COLLECTION_CLOSE_AND_SPACER = """\
      </div>
      <div class="es-100"></div>"""


def display_name(speaker: dict) -> str:
    return f"{speaker['name']} {speaker.get('surname', '')}".strip()


def make_slug(speaker: dict) -> str:
    return speaker.get("slug", display_name(speaker).lower().replace(" ", "-"))


def speaker_photo(speaker: dict) -> str:
    """Return best available photo path/URL."""
    if speaker.get("photo"):
        return speaker["photo"]
    if speaker.get("pretalx_photo"):
        return speaker["pretalx_photo"]
    return ""


def build_item(speaker: dict) -> str:
    """Build one collection-item div for the speakers grid."""
    slug = make_slug(speaker)
    name = escape(display_name(speaker))
    company = escape(speaker.get("company", ""))
    photo = speaker_photo(speaker)
    detail_url = f"speakers/{slug}.html"

    photo_tag = (
        f'<img src="{escape(photo)}" loading="lazy" alt="{name}" class="speaker-img">'
        if photo
        else '<img src="images/placeholder-speaker.svg" loading="lazy" alt="" class="speaker-img">'
    )

    return f"""\
          <div class="collection-item">
            <a href="{detail_url}" class="speaker-link w-inline-block">
              <div class="speaker-img-overlay"></div>{photo_tag}
            </a>
            <a href="{detail_url}" class="speaker-name-link w-inline-block">
              <div class="speaker-name">{name}</div>
            </a>
            <div class="speaker-title">{company}</div>
          </div>"""


def main():
    speakers = json.loads(SPEAKERS_JSON.read_text())
    html = SPEAKERS_HTML.read_text()

    items = "\n".join(build_item(s) for s in speakers)

    # Find the speakers-collection div and replace everything between it
    # and the es-100 spacer that follows
    start = html.index(COLLECTION_OPEN)
    # Find the es-100 spacer after the collection
    end = html.index(COLLECTION_CLOSE_AND_SPACER, start)

    new_block = f"""\
{COLLECTION_OPEN}
        <div class="collection-list speakers-list">
{items}
        </div>
{COLLECTION_CLOSE_AND_SPACER}"""

    html = html[:start] + new_block + html[end + len(COLLECTION_CLOSE_AND_SPACER):]

    SPEAKERS_HTML.write_text(html)
    print(f"Done: {len(speakers)} speakers stamped into speakers.html")


if __name__ == "__main__":
    main()
