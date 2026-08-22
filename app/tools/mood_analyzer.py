"""Scene Mood Analyzer - uses Google GenAI SDK."""

import os
from google import genai


class MoodAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.use_ai = False
            self.client = None

    def analyze_mood(self, scene_text: str) -> dict:
        if self.use_ai:
            try:
                prompt = f"Analyze the mood of this scene: {scene_text}. Return mood, emoji, intensity, music, colors."
                response = self.client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                return {"mood": response.text.strip(), "ai": True}
            except Exception:
                pass
        return self._basic_analyze(scene_text)

    def _basic_analyze(self, scene_text: str) -> dict:
        text_lower = scene_text.lower()
        if "night" in text_lower or "dark" in text_lower:
            mood, emoji = "Mysterious/Tense", "🌙"
        elif "love" in text_lower or "kiss" in text_lower:
            mood, emoji = "Romantic", "❤️"
        else:
            mood, emoji = "Neutral", "😐"
        return {"mood": mood, "emoji": emoji, "ai": False}

    def analyze_screenplay(self, screenplay: str) -> list:
        scenes = [l.strip() for l in screenplay.split("\n") if l.strip().startswith(("INT.", "EXT."))]
        results = []
        for i, scene in enumerate(scenes):
            r = self.analyze_mood(scene)
            r["scene_number"] = i + 1
            r["heading"] = scene
            results.append(r)
        return results

    def format_results(self, results: list) -> str:
        lines = ["🎭 Scene Mood Analysis", "=" * 40]
        for r in results:
            lines.append(f"Scene {r['scene_number']}: {r['heading']}")
            lines.append(f"  Mood: {r['mood']}")
        return "\n".join(lines)
