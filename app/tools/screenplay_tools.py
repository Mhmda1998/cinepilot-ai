"""Tools for CinePilot AI screenplay analysis."""

import re
from typing import Any


def analyze_screenplay(screenplay: str) -> dict[str, Any]:
    """Analyze a screenplay and extract structured production data."""

    if not screenplay or not screenplay.strip():
        return {
            "success": False,
            "error": "Screenplay text is empty.",
        }

    text = screenplay.strip()

    # Detect screenplay scene headings.
    scene_pattern = re.compile(
        r"(?im)^(?:INT\.|EXT\.|INT/EXT\.)\s+.+$"
    )

    scenes = []

    for line in text.splitlines():
        line = line.strip()

        if scene_pattern.match(line):
            parts = re.split(r"\s+-\s+", line, maxsplit=1)

            heading = line

            if len(parts) == 2:
                location = parts[0]
                time_of_day = parts[1].strip().upper()
            else:
                location = line
                time_of_day = "UNKNOWN"

            scenes.append(
                {
                    "heading": heading,
                    "location": location,
                    "time_of_day": time_of_day,
                }
            )

    # Extract characters only from uppercase dialogue headings.
    characters = []

    for line in text.splitlines():
        name = line.strip()

        if not name:
            continue

        # Never classify scene headings as characters.
        if scene_pattern.match(name):
            continue

        # Character names are uppercase and reasonably short.
        if (
            name == name.upper()
            and re.fullmatch(r"[A-Z][A-Z0-9 .'-]{1,40}", name)
            and not re.search(r"\s-\s", name)
            and name not in {
                "DAY",
                "NIGHT",
                "MORNING",
                "EVENING",
                "DUSK",
                "DAWN",
            }
        ):
            if name not in characters:
                characters.append(name)

    return {
        "success": True,
        "scene_count": len(scenes),
        "scenes": scenes,
        "characters": characters,
        "character_count": len(characters),
    }
