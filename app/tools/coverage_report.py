"""Script Coverage Report - تقرير تغطية سيناريو احترافي."""

import os


class CoverageReport:
    """Generate professional script coverage report."""

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

    def generate_coverage(self, screenplay: str, production_data: dict) -> str:
        """Generate coverage report."""
        if self.use_ai:
            return self._ai_coverage(screenplay, production_data)
        return self._basic_coverage(production_data)

    def _ai_coverage(self, screenplay: str, production_data: dict) -> str:
        """AI-powered coverage report."""
        prompt = f"""
        Create a professional script coverage report for this screenplay.
        Include: Logline, Genre, Strengths, Weaknesses, Recommendation.
        
        Screenplay data:
        Scenes: {len(production_data.get("scenes", []))}
        Characters: {production_data.get("characters", [])}
        Props: {production_data.get("props", [])}
        
        Keep it professional and brief.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return self._basic_coverage(production_data)

    def _basic_coverage(self, data: dict) -> str:
        """Basic coverage without AI."""
        lines = ["📄 Script Coverage Report", "=" * 40]
        lines.append(f"Scenes: {len(data.get('scenes', []))}")
        lines.append(f"Characters: {len(data.get('characters', []))}")
        lines.append(f"Props: {len(data.get('props', []))}")
        lines.append(f"Wardrobe: {len(data.get('wardrobe', []))}")
        lines.append(f"Locations: {len(data.get('locations', []))}")
        lines.append("")
        lines.append("Recommendation: CONSIDER")
        return "\n".join(lines)
