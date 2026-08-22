"""Dialogue Emotion Analyzer - uses Google GenAI SDK."""

import os
from google import genai


class EmotionAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.use_ai = False
            self.client = None

    def analyze_dialogue(self, dialogue: str) -> dict:
        if self.use_ai:
            try:
                prompt = f"Analyze emotion in this dialogue: {dialogue}"
                response = self.client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                return {"emotion": response.text.strip(), "ai": True}
            except Exception:
                pass
        d = dialogue.lower()
        if "hate" in d:
            emotion = "Angry"
        elif "love" in d:
            emotion = "Romantic"
        else:
            emotion = "Neutral"
        return {"emotion": emotion, "ai": False}

    def analyze_scene_dialogues(self, production_data: dict) -> list:
        results = []
        for d in production_data.get("dialogue", []):
            r = self.analyze_dialogue(d.get("text", ""))
            r["character"] = d.get("character", "Unknown")
            r["dialogue"] = d.get("text", "")
            results.append(r)
        return results

    def format_results(self, results: list) -> str:
        lines = ["💬 Dialogue Emotion Analysis", "=" * 40]
        for r in results:
            lines.append(f"{r.get('character', '')}: {r.get('emotion', '')}")
        return "\n".join(lines)
