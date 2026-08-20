"""Tools for CinePilot AI screenplay analysis."""

import re
from typing import Any


TIME_OF_DAY = {
    "DAY",
    "NIGHT",
    "MORNING",
    "EVENING",
    "DUSK",
    "DAWN",
}


SCENE_PATTERN = re.compile(
    r"^(INT\.|EXT\.|INT/EXT\.)\s+(.+?)(?:\s+-\s+(DAY|NIGHT|MORNING|EVENING|DUSK|DAWN))?$",
    re.IGNORECASE,
)


CHARACTER_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9 .'-]{1,40}$"
)


def _extract_scenes(text: str) -> list[dict[str, Any]]:
    """Extract screenplay scene headings."""

    scenes = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        match = SCENE_PATTERN.match(line)

        if not match:
            continue

        prefix = match.group(1).upper()
        location = match.group(2).strip()
        time_of_day = (
            match.group(3).upper()
            if match.group(3)
            else "UNKNOWN"
        )

        scenes.append(
            {
                "scene_number": len(scenes) + 1,
                "heading": line,
                "type": prefix,
                "location": location,
                "time_of_day": time_of_day,
            }
        )

    return scenes


def _extract_characters(text: str) -> list[str]:
    """Extract conservative uppercase character headings."""

    characters = []

    ignored = {
        "DAY",
        "NIGHT",
        "MORNING",
        "EVENING",
        "DUSK",
        "DAWN",
        "FADE IN",
        "FADE OUT",
        "CUT TO",
    }

    for raw_line in text.splitlines():
        name = raw_line.strip()

        if not name:
            continue

        # Scene headings are never characters.
        if SCENE_PATTERN.match(name):
            continue

        if name in ignored:
            continue

        if not CHARACTER_PATTERN.fullmatch(name):
            continue

        # Avoid obvious screenplay transitions.
        if name.startswith(("FADE ", "CUT ", "DISSOLVE ")):
            continue

        if name not in characters:
            characters.append(name)

    return characters


def _extract_dialogue(
    text: str,
    characters: list[str],
) -> list[dict[str, Any]]:
    """Extract dialogue associated with character headings."""

    dialogue = []
    current_character = None
    current_lines = []

    character_set = set(characters)

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            if current_character and current_lines:
                dialogue.append(
                    {
                        "character": current_character,
                        "text": " ".join(current_lines),
                    }
                )
                current_character = None
                current_lines = []

            continue

        if SCENE_PATTERN.match(line):
            if current_character and current_lines:
                dialogue.append(
                    {
                        "character": current_character,
                        "text": " ".join(current_lines),
                    }
                )

            current_character = None
            current_lines = []
            continue

        if line in character_set:
            if current_character and current_lines:
                dialogue.append(
                    {
                        "character": current_character,
                        "text": " ".join(current_lines),
                    }
                )

            current_character = line
            current_lines = []
            continue

        if current_character:
            current_lines.append(line)

    if current_character and current_lines:
        dialogue.append(
            {
                "character": current_character,
                "text": " ".join(current_lines),
            }
        )

    return dialogue


def _extract_actions(
    text: str,
    characters: list[str],
) -> list[str]:
    """Extract likely action lines."""

    actions = []

    character_set = set(characters)

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if SCENE_PATTERN.match(line):
            continue

        if line in character_set:
            continue

        # Skip dialogue lines by checking whether they occur
        # immediately after a character heading.
        if line.startswith('"') and line.endswith('"'):
            continue

        if line not in actions:
            actions.append(line)

    return actions


def analyze_screenplay(
    screenplay: str,
) -> dict[str, Any]:
    """Analyze screenplay structure."""

    if not screenplay or not screenplay.strip():
        return {
            "success": False,
            "error": "Screenplay text is empty.",
        }

    text = screenplay.strip()

    scenes = _extract_scenes(text)
    characters = _extract_characters(text)

    return {
        "success": True,
        "scene_count": len(scenes),
        "scenes": scenes,
        "characters": characters,
        "character_count": len(characters),
    }


def production_breakdown(
    screenplay: str,
) -> dict[str, Any]:
    """Build a structured production breakdown."""

    if not screenplay or not screenplay.strip():
        return {
            "success": False,
            "error": "Screenplay text is empty.",
        }

    text = screenplay.strip()

    scenes = _extract_scenes(text)
    characters = _extract_characters(text)
    dialogue = _extract_dialogue(text, characters)

    locations = []
    time_of_day = []

    for scene in scenes:
        location = scene["location"]

        if location not in locations:
            locations.append(location)

        tod = scene["time_of_day"]

        if tod not in time_of_day:
            time_of_day.append(tod)

    return {
        "success": True,
        "scene_count": len(scenes),
        "scenes": scenes,
        "characters": characters,
        "character_count": len(characters),
        "locations": locations,
        "location_count": len(locations),
        "time_of_day": time_of_day,
        "dialogue": dialogue,
        "production_facts": {
            "speaking_characters": characters,
            "locations": locations,
            "time_of_day": time_of_day,
        },
        "production_inferences": [],
    }
