"""Dialogue Emotion Analyzer - يحلل مشاعر الحوار بين الشخصيات."""

import os


class EmotionAnalyzer:
    """Analyze emotions in dialogue."""

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

    def analyze_dialogue(self, dialogue: str) -> dict:
        """Analyze emotion in dialogue text."""
        if self.use_ai:
            try:
                prompt = f"Analyze the emotion in this dialogue: {dialogue}\nReturn only the emotion name (e.g., Angry, Sad, Romantic, Tense, Neutral)."
                response = self.model.generate_content(prompt)
                return {"emotion": response.text.strip(), "ai": True}
            except:
                pass
        
        # Basic fallback
        d = dialogue.lower()
        if any(word in d for word in ["love", "kiss", "hug"]):
            emotion = "Romantic"
        elif any(word in d for word in ["angry", "hate", "leave"]):
            emotion = "Angry"
        elif any(word in d for word in ["cry", "sad", "miss"]):
            emotion = "Sad"
        elif any(word in d for word in ["fear", "scared", "dark"]):
            emotion = "Fearful"
        else:
            emotion = "Neutral"
        
        return {"emotion": emotion, "ai": False}

    def analyze_scene_dialogues(self, production_data: dict) -> list:
        """Analyze emotions for all dialogues."""
        dialogues = production_data.get("dialogue", [])
        results = []
        for d in dialogues:
            text = d.get("text", "")
            character = d.get("character", "Unknown")
            emotion = self.analyze_dialogue(text)
            results.append({
                "character": character,
                "dialogue": text,
                "emotion": emotion["emotion"]
            })
        return results

    def format_results(self, results: list) -> str:
        lines = ["💬 Dialogue Emotion Analysis", "=" * 50]
        for r in results:
            lines.append(f"\n{r['character']}: {r['dialogue']}")
            lines.append(f"  Emotion: {r['emotion']}")
        return "\n".join(lines)
