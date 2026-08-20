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
    """Extract action lines while excluding screenplay dialogue."""

    actions = []

    scene_pattern = re.compile(
        r"(?i)^(?:INT\\.|EXT\\.|INT/EXT\\.)\\s+.+$"
    )

    character_names = {
        character.strip().upper()
        for character in characters
        if character and character.strip()
    }

    lines = text.splitlines()

    in_dialogue = False

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            in_dialogue = False
            continue

        # Scene heading.
        if scene_pattern.match(line):
            in_dialogue = False
            continue

        # Character heading.
        if line.upper() in character_names:
            in_dialogue = True
            continue

        # Parenthetical dialogue direction.
        if in_dialogue:
            if (
                line.startswith("(")
                or line.startswith("[")
            ):
                continue

            # Dialogue continues until a blank line.
            continue

        # Skip standalone uppercase screenplay headings.
        if (
            line == line.upper()
            and re.fullmatch(
                r"[A-Z][A-Z0-9 .'-]{1,40}",
                line,
            )
        ):
            continue

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



def _extract_props(
    text: str,
    characters: list[str],
) -> list[str]:
    """Extract explicitly mentioned handheld or used props."""

    actions = _extract_actions(text, characters)

    props = []

    patterns = [
        r"\b(?:holds?|holding|carries?|carrying)\s+(?:a|an|the)\s+([A-Za-z][A-Za-z0-9 -]{1,40})",
        r"\b(?:picks up|pick up|grabs?|takes?)\s+(?:a|an|the)\s+([A-Za-z][A-Za-z0-9 -]{1,40})",
        r"\b(?:opens?|opening|closes?|closing)\s+(?:a|an|the)\s+([A-Za-z][A-Za-z0-9 -]{1,40})",
    ]

    stop_words = {
        "from",
        "to",
        "into",
        "onto",
        "with",
        "and",
        "then",
        "while",
        "before",
        "after",
    }

    for action in actions:
        for pattern in patterns:
            for match in re.finditer(
                pattern,
                action,
                re.IGNORECASE,
            ):
                prop = match.group(1).strip()

                words = prop.split()
                cleaned_words = []

                for word in words:
                    if word.lower() in stop_words:
                        break
                    cleaned_words.append(word)

                prop = " ".join(cleaned_words).strip()

                if not prop:
                    continue

                if prop.lower() not in {
                    item.lower() for item in props
                }:
                    props.append(prop)

    return props


def _extract_wardrobe(
    text: str,
    characters: list[str],
) -> list[str]:
    """Extract explicitly mentioned wardrobe or clothing."""

    actions = _extract_actions(text, characters)

    wardrobe = []

    patterns = [
        r"\bwears?\s+(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,50})",
        r"\bwearing\s+(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,50})",
        r"\bdressed in\s+(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,50})",
        r"\bputs on\s+(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,50})",
    ]

    stop_words = {
        "and",
        "then",
        "while",
        "as",
        "before",
        "after",
        "with",
        "while",
    }

    for action in actions:
        for pattern in patterns:
            for match in re.finditer(
                pattern,
                action,
                re.IGNORECASE,
            ):
                item = match.group(1).strip()

                words = item.split()
                cleaned_words = []

                for word in words:
                    if word.lower() in stop_words:
                        break
                    cleaned_words.append(word)

                item = " ".join(cleaned_words).strip()

                # Normalize references such as:
                # "same black jacket" -> "black jacket"
                item = re.sub(
                    r"^(?:the\s+)?same\s+",
                    "",
                    item,
                    flags=re.IGNORECASE,
                ).strip()

                if not item:
                    continue

                if item.lower() not in {
                    value.lower() for value in wardrobe
                }:
                    wardrobe.append(item)

    return wardrobe


def _extract_sound(
    text: str,
    characters: list[str],
) -> list[str]:
    """Extract explicitly mentioned sound or audio cues."""

    actions = _extract_actions(text, characters)

    sounds = []

    patterns = [
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:ring|rings|ringing)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:slam|slams|slamming)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:echo|echoes|echoing)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:rumble|rumbles|rumbling)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:start|starts|starting)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:crash|crashes|crashing)\b",
        r"\b(?:a|an|the)?\s*([A-Za-z][A-Za-z0-9 -]{1,40})\s+(?:click|clicks|clicking)\b",
    ]

    for action in actions:
        for pattern in patterns:
            for match in re.finditer(
                pattern,
                action,
                re.IGNORECASE,
            ):
                sound = match.group(1).strip()

                sound = re.sub(
                    r"^(?:a|an|the)\s+",
                    "",
                    sound,
                    flags=re.IGNORECASE,
                ).strip()

                sound = sound.lower()

                if not sound:
                    continue

                if sound not in {
                    value.lower() for value in sounds
                }:
                    sounds.append(sound)

    return sounds


def _extract_lighting(
    text: str,
    characters: list[str],
) -> list[str]:
    """Extract explicitly mentioned lighting cues."""

    actions = _extract_actions(text, characters)

    lighting = []

    patterns = [
        r"\b((?:bright|dim|dark|soft|harsh|warm|cold|red|blue|green|white|natural|neon)\s+lights?)\b",
        r"\b((?:bright|dim|dark|soft|harsh|warm|cold|red|blue|green|white|natural|neon)\s+lighting)\b",
        r"\b((?:flashlight|candlelight|sunlight|moonlight|streetlight|spotlight))\b",
        r"\b(?:lit by|illuminated by|bathed in)\s+((?:bright|dim|soft|harsh|warm|cold|red|blue|green|white|natural|neon)\s+lights?)\b",
    ]

    for action in actions:
        for pattern in patterns:
            for match in re.finditer(
                pattern,
                action,
                re.IGNORECASE,
            ):
                item = match.group(1).strip().lower()

                if not item:
                    continue

                if item not in {
                    value.lower() for value in lighting
                }:
                    lighting.append(item)

    return lighting

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
    actions = _extract_actions(text, characters)
    props = _extract_props(text, characters)
    wardrobe = _extract_wardrobe(text, characters)
    sounds = _extract_sound(text, characters)
    lighting = _extract_lighting(text, characters)
    lighting = _extract_lighting(text, characters)

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
        "actions": actions,
        "props": props,
        "wardrobe": wardrobe,
        "sounds": sounds,
        "lighting": lighting,
        "lighting": lighting,
        "production_facts": {
            "speaking_characters": characters,
            "locations": locations,
            "time_of_day": time_of_day,
            "actions": actions,
            "props": props,
            "wardrobe": wardrobe,
            "sounds": sounds,
            "lighting": lighting,
            "lighting": lighting,
        },
        "production_inferences": [],
    }
