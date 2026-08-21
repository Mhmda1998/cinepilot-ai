"""Gemini-powered screenplay analyzer - uses real AI."""

import os
import json
from typing import Any

import google.generativeai as genai


class GeminiAnalyzer:
    """Use Gemini to analyze screenplay text intelligently."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-3.6-flash")
            self.is_ready = True
        else:
            self.model = None
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
            response = self.model.generate_content(prompt)
            text = response.text
            
            # تنظيف النص لاستخراج JSON
            text = text.strip()
            
            # إزالة علامات markdown إذا وجدت
            if text.startswith("```"):
                text = text.split("\n", 1)[-1]
                text = text.rsplit("```", 1)[0]
            
            text = text.strip()
            
            # تحويل إلى dict
            data = json.loads(text)
            return {"success": True, **data}
            
        except json.JSONDecodeError as e:
            # إذا فشل JSON، نرجع النص كما هو
            return {
                "success": True,
                "raw_text": response.text,
                "error": f"JSON parse failed: {e}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def analyze_with_gemini(screenplay: str) -> dict[str, Any]:
    """Quick function to analyze screenplay with Gemini."""
    analyzer = GeminiAnalyzer()
    return analyzer.analyze(screenplay)
