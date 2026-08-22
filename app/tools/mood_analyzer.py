"""Scene Mood Analyzer - يحلل المشاعر في كل مشهد."""

import os


class MoodAnalyzer:
    """Analyze emotional mood for each scene in screenplay."""

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

    def analyze_mood(self, scene_text: str) -> dict:
        """Analyze mood for a single scene."""
        if self.use_ai:
            return self._ai_analyze(scene_text)
        return self._basic_analyze(scene_text)

    def _ai_analyze(self, scene_text: str) -> dict:
        """Use AI to analyze scene mood."""
        prompt = f"""
        Analyze the emotional mood of this film scene:
        {scene_text}
        
        Return JSON with:
        {{
            "mood": "primary emotion (Happy/Sad/Tense/Romantic/Scary/Mysterious/Exciting)",
            "emoji": "matching emoji",
            "intensity": 1-10,
            "music_suggestion": "music genre that fits",
            "color_palette": "suggested colors"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            return {"mood": response.text, "ai": True}
        except:
            return self._basic_analyze(scene_text)

    def _basic_analyze(self, scene_text: str) -> dict:
        """Basic mood analysis without AI."""
        text_lower = scene_text.lower()
        
        if any(word in text_lower for word in ["dark", "night", "shadow"]):
            mood = "Mysterious/Tense"
            emoji = "🌙"
        elif any(word in text_lower for word in ["love", "kiss", "embrace"]):
            mood = "Romantic"
            emoji = "❤️"
        elif any(word in text_lower for word in ["chase", "run", "fight"]):
            mood = "Exciting/Action"
            emoji = "⚡"
        elif any(word in text_lower for word in ["cry", "death", "sad"]):
            mood = "Sad"
            emoji = "😢"
        else:
            mood = "Neutral"
            emoji = "😐"
        
        return {
            "mood": mood,
            "emoji": emoji,
            "intensity": 5,
            "music_suggestion": "Depends on scene",
            "color_palette": "Depends on scene",
            "ai": False
        }

    def analyze_screenplay(self, screenplay: str) -> list:
        """Analyze mood for all scenes."""
        scenes = self._extract_scenes(screenplay)
        results = []
        
        for i, scene in enumerate(scenes):
            analysis = self.analyze_mood(scene)
            analysis["scene_number"] = i + 1
            analysis["heading"] = scene
            results.append(analysis)
        
        return results

    def _extract_scenes(self, text: str) -> list:
        """Extract scene headings."""
        scenes = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("INT.") or line.startswith("EXT."):
                scenes.append(line)
        return scenes

    def format_results(self, results: list) -> str:
        """Format mood analysis results."""
        lines = ["🎭 Scene Mood Analysis", "=" * 40]
        for r in results:
            lines.append(f"\nScene {r['scene_number']}: {r['heading']}")
            lines.append(f"  Mood: {r['mood']}")
            if "emoji" in r:
                lines.append(f"  Emoji: {r['emoji']}")
        return "\n".join(lines)
