"""AI Casting Suggestions - uses Google GenAI SDK."""

import os
from google import genai


class CastingSuggestor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.use_ai = False
            self.client = None

    def suggest_casting(self, characters: list) -> dict:
        suggestions = {}
        for character in characters:
            if self.use_ai:
                try:
                    prompt = f"Suggest actor archetype for character {character}"
                    response = self.client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                    suggestions[character] = response.text.strip()
                except Exception:
                    suggestions[character] = "Versatile actor"
            else:
                suggestions[character] = "Versatile actor"
        return suggestions

    def format_suggestions(self, suggestions: dict) -> str:
        lines = ["👤 Casting Suggestions", "=" * 40]
        for char, sugg in suggestions.items():
            lines.append(f"{char}: {sugg}")
        return "\n".join(lines)
