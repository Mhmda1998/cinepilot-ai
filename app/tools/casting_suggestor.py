"""AI Casting Suggestions - يقترح ممثلين للأدوار."""

import os


class CastingSuggestor:
    """Suggest actor types for characters in screenplay."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        
        if self.api_key:
            self.use_ai = True
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-3.6-flash")
        else:
            self.use_ai = False
            self.model = None

    def suggest_casting(self, characters: list) -> dict:
        """Suggest actor archetypes for each character."""
        suggestions = {}
        
        for character in characters:
            if self.use_ai:
                suggestion = self._ai_suggest(character)
            else:
                suggestion = self._basic_suggest(character)
            
            suggestions[character] = suggestion
        
        return suggestions

    def _ai_suggest(self, character: str) -> str:
        """Use AI to suggest actor type."""
        prompt = f"""
        For the character named "{character}" in a film:
        Suggest actor archetype (age, type, personality traits).
        Keep it brief: 2-3 lines.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return self._basic_suggest(character)

    def _basic_suggest(self, character: str) -> str:
        """Basic suggestion without AI."""
        return f"Character: {character}\nSuggested: Versatile actor, age flexible"

    def format_suggestions(self, suggestions: dict) -> str:
        """Format casting suggestions."""
        lines = ["👤 Casting Suggestions", "=" * 40]
        for character, suggestion in suggestions.items():
            lines.append(f"\n{character}:")
            lines.append(f"  {suggestion}")
        return "\n".join(lines)
