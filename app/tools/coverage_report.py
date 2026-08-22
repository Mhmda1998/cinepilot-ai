"""Script Coverage Report - uses Google GenAI SDK."""

import os
from google import genai


class CoverageReport:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.use_ai = False
            self.client = None

    def generate_coverage(self, screenplay: str, production_data: dict) -> str:
        if self.use_ai:
            try:
                prompt = f"Create a script coverage report for this screenplay: {screenplay}"
                response = self.client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                return response.text.strip()
            except Exception:
                pass
        lines = ["📄 Script Coverage Report", "=" * 40]
        lines.append(f"Scenes: {len(production_data.get('scenes', []))}")
        lines.append(f"Characters: {', '.join(production_data.get('characters', []))}")
        lines.append("Recommendation: CONSIDER")
        return "\n".join(lines)
