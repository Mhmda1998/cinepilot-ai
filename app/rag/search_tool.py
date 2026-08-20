from __future__ import annotations

from typing import Any

from .retriever import ScreenplayRetriever


_retriever = ScreenplayRetriever()


def index_screenplay(chunks: list[str]) -> dict[str, Any]:
    """Index screenplay chunks for semantic search."""

    if not chunks:
        return {
            "success": False,
            "error": "No screenplay chunks provided.",
        }

    _retriever.index(chunks)

    return {
        "success": True,
        "chunk_count": len(_retriever.chunks),
    }


def search_screenplay(
    query: str,
    top_k: int = 3,
) -> dict[str, Any]:
    """Search the indexed screenplay semantically."""

    if not query or not query.strip():
        return {
            "success": False,
            "error": "Search query is empty.",
        }

    if not _retriever.chunks:
        return {
            "success": False,
            "error": "No screenplay has been indexed yet.",
        }

    results = _retriever.search(
        query=query,
        top_k=top_k,
    )

    return {
        "success": True,
        "query": query,
        "result_count": len(results),
        "results": results,
    }
