"""Production Bible - يدمج كل تقارير الإنتاج في تقرير واحد."""

import os


class ProductionBible:
    """Generate a unified production report from all tools."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")

    def generate_full_report(self, screenplay: str) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("PRODUCTION BIBLE - CINEPILOT AI")
        lines.append("=" * 70)

        # Import production data once
        from app.tools.screenplay_tools import production_breakdown
        try:
            data = production_breakdown(screenplay)
        except Exception as e:
            data = {}
            lines.append(f"Error in production breakdown: {e}")

        # 1. Basic Analysis
        lines.append("")
        lines.append("### 1. Screenplay Analysis")
        lines.append("-" * 40)
        try:
            from app.tools.screenplay_tools import analyze_screenplay
            analysis = analyze_screenplay(screenplay)
            if analysis.get("success"):
                lines.append(f"Scenes: {analysis.get('scene_count', 0)}")
                chars = analysis.get('characters', [])
                lines.append(f"Characters: {', '.join(chars) if chars else 'None'}")
        except Exception as e:
            lines.append(f"Error: {e}")

        # 2. Production Breakdown
        lines.append("")
        lines.append("### 2. Production Breakdown")
        lines.append("-" * 40)
        if data.get("success"):
            lines.append(f"Locations: {', '.join(data.get('locations', [])) or 'None'}")
            lines.append(f"Props: {', '.join(data.get('props', [])) or 'None'}")
            lines.append(f"Wardrobe: {', '.join(data.get('wardrobe', [])) or 'None'}")
            lines.append(f"Sound: {', '.join(data.get('sounds', [])) or 'None'}")
            lines.append(f"Lighting: {', '.join(data.get('lighting', [])) or 'None'}")
        else:
            lines.append("No production data available.")

        # 3. Coverage Report
        lines.append("")
        lines.append("### 3. Script Coverage Report")
        lines.append("-" * 40)
        try:
            from app.tools.coverage_report import CoverageReport
            coverage = CoverageReport()
            report = coverage.generate_coverage(screenplay, data)
            lines.append(report)
        except Exception as e:
            lines.append(f"Error: {e}")

        # 4. Mood Analysis
        lines.append("")
        lines.append("### 4. Scene Mood Analysis")
        lines.append("-" * 40)
        try:
            from app.tools.mood_analyzer import MoodAnalyzer
            mood = MoodAnalyzer()
            results = mood.analyze_screenplay(screenplay)
            lines.append(mood.format_results(results))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 5. Dialogue Emotion
        lines.append("")
        lines.append("### 5. Dialogue Emotion Analysis")
        lines.append("-" * 40)
        try:
            from app.tools.dialogue_emotion_analyzer import EmotionAnalyzer
            emotion = EmotionAnalyzer()
            results = emotion.analyze_scene_dialogues(data)
            lines.append(emotion.format_results(results))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 6. Camera Angles
        lines.append("")
        lines.append("### 6. Camera Angle Suggestions")
        lines.append("-" * 40)
        try:
            from app.tools.camera_suggestor import CameraSuggestor
            camera = CameraSuggestor()
            results = camera.suggest_all(screenplay)
            lines.append(camera.format_results(results))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 7. Shooting Schedule
        lines.append("")
        lines.append("### 7. Shooting Schedule")
        lines.append("-" * 40)
        try:
            from app.tools.shooting_schedule import ShootingSchedule
            schedule = ShootingSchedule()
            scenes = data.get('scenes', [])
            result = schedule.generate_schedule(scenes)
            lines.append(schedule.format_schedule(result))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 8. Budget Estimate
        lines.append("")
        lines.append("### 8. Budget Estimate")
        lines.append("-" * 40)
        try:
            from app.tools.budget_estimator import BudgetEstimator
            budget = BudgetEstimator()
            result = budget.estimate_budget(data)
            lines.append(budget.format_budget(result))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 9. Casting Suggestions
        lines.append("")
        lines.append("### 9. Casting Suggestions")
        lines.append("-" * 40)
        try:
            from app.tools.casting_suggestor import CastingSuggestor
            casting = CastingSuggestor()
            result = casting.suggest_casting(data.get('characters', []))
            lines.append(casting.format_suggestions(result))
        except Exception as e:
            lines.append(f"Error: {e}")

        # 10. Continuity Report
        lines.append("")
        lines.append("### 10. Continuity Report")
        lines.append("-" * 40)
        try:
            from app.tools.continuity_tracker import ContinuityTracker
            continuity = ContinuityTracker()
            lines.append(continuity.generate_report(data))
        except Exception as e:
            lines.append(f"Error: {e}")

        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF REPORT")
        return "\n".join(lines)
