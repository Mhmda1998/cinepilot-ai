from __future__ import annotations

from google import genai


DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


class GeminiEmbedder:
    """Generate Gemini embeddings for CinePilot RAG."""

    def __init__(
        self,
        model: str = DEFAULT_EMBEDDING_MODEL,
        client=None,
    ):
        self.model = model
        self.client = client or genai.Client()

    def embed(self, text: str) -> list[float]:
        """Generate an embedding for one text."""

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        if not response.embeddings:
            raise RuntimeError(
                "Gemini returned no embedding."
            )

        return list(response.embeddings[0].values)

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        if not texts:
            return []

        return [
            self.embed(text)
            for text in texts
        ]
