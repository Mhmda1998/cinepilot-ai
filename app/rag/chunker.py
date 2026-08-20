from __future__ import annotations

import re


SCENE_HEADING_PATTERN = re.compile(
    r"^(?:INT\.|EXT\.|INT/EXT\.)\s+.+$",
    re.IGNORECASE,
)


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    """
    Split screenplay text into semantic chunks.

    A chunk never crosses a screenplay scene boundary.
    """

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()

    scenes = _extract_scenes(normalized)

    chunks = []

    for scene in scenes:
        chunks.extend(
            _chunk_single_scene(
                scene,
                chunk_size,
            )
        )

    return chunks


def _extract_scenes(text: str) -> list[str]:
    """Split screenplay into individual scenes."""

    lines = text.splitlines()

    scenes = []
    current = []

    for raw_line in lines:
        line = raw_line.strip()

        if SCENE_HEADING_PATTERN.match(line):
            if current:
                scene = "\n".join(current).strip()

                if scene:
                    scenes.append(scene)

            current = [line]

        elif current:
            current.append(raw_line)

    if current:
        scene = "\n".join(current).strip()

        if scene:
            scenes.append(scene)

    return scenes or [text]


def _chunk_single_scene(
    scene: str,
    chunk_size: int,
) -> list[str]:
    """Split one scene without crossing its boundary."""

    if len(scene) <= chunk_size:
        return [scene]

    blocks = [
        block.strip()
        for block in re.split(r"\n\s*\n", scene)
        if block.strip()
    ]

    chunks = []
    current = []

    for block in blocks:
        candidate = "\n\n".join(current + [block])

        if current and len(candidate) > chunk_size:
            chunks.append("\n\n".join(current))
            current = []

        if len(block) > chunk_size:
            if current:
                chunks.append("\n\n".join(current))
                current = []

            chunks.extend(
                _split_large_block(block, chunk_size)
            )
            continue

        current.append(block)

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _split_large_block(
    block: str,
    chunk_size: int,
) -> list[str]:
    """Split a large block without cutting words."""

    words = block.split()

    chunks = []
    current = []

    for word in words:
        candidate = " ".join(current + [word])

        if current and len(candidate) > chunk_size:
            chunks.append(" ".join(current))
            current = []

        current.append(word)

    if current:
        chunks.append(" ".join(current))

    return chunks
