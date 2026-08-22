"""Gemini-powered screenplay analyzer - uses Google GenAI SDK."""

import os
import json
from typing import Any

from google import genai


class GeminiAnalyzer:
    """Use Gemini to analyze screenplay text intelligently."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.is_ready = True
        else:
            self.client = None
            self.is_ready = False

    def analyze(self, screenplay: str) -> dict[str, Any]:
        """Analyze screenplay using Gemini AI."""
        if not self.is_ready:
            return {"success": False, "error": "No API key"}

        prompt = f"""
You are a film production analyzer. Analyze this screenplay and extract production data.

Return ONLY valid JSON with this exact structure:
{{
    "scenes": [{{"heading": "scene heading", "location": "location", "time": "time of day"}}],
    "characters": ["character names"],
    "props": ["props mentioned"],
    "wardrobe": ["clothing items"],
    "sounds": ["sound effects"],
    "lighting": ["lighting cues"],
    "actions": ["important actions"]
}}

Rules:
- Extract ONLY what is explicitly written
- Do not invent or assume
- If something is not present, return empty list

Screenplay:
{screenplay}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            text = response.text.strip()

            # إزالة علامات markdown إذا وُجدت
            if text.startswith("```"):
                text = text.split("\n", 1)[-1]
                text = text.rsplit("```", 1)[0]
            text = text.strip()

            data = json.loads(text)
            return {"success": True, **data}

        except json.JSONDecodeError as e:
            return {
                "success": True,
                "raw_text": response.text if 'response' in locals() else "",
                "error": f"JSON parse failed: {e}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def analyze_with_gemini(screenplay: str) -> dict[str, Any]:
    """Quick function to analyze screenplay with Gemini."""
    analyzer = GeminiAnalyzer()
    return analyzer.analyze(screenplay)
