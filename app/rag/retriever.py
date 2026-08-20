from __future__ import annotations

import math
from typing import Any

from .embeddings import GeminiEmbedder


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculate cosine similarity between two vectors."""

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Vectors must have the same dimensions."
        )

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    norm_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class ScreenplayRetriever:
    """Semantic retriever for CinePilot screenplay chunks."""

    def __init__(
        self,
        embedder: GeminiEmbedder | None = None,
    ):
        self.embedder = embedder or GeminiEmbedder()
        self.chunks: list[str] = []
        self.embeddings: list[list[float]] = []

    def index(self, chunks: list[str]) -> None:
        """Create embeddings for screenplay chunks."""

        self.chunks = [
            chunk.strip()
            for chunk in chunks
            if chunk and chunk.strip()
        ]

        if not self.chunks:
            self.embeddings = []
            return

        self.embeddings = self.embedder.embed_many(
            self.chunks
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """Return the most semantically relevant chunks."""

        if not query or not query.strip():
            return []

        if not self.chunks:
            return []

        query_embedding = self.embedder.embed(query)

        results = []

        for index, embedding in enumerate(self.embeddings):
            score = cosine_similarity(
                query_embedding,
                embedding,
            )

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": score,
                    "index": index,
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:max(1, top_k)]
