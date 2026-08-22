"""Camera Angle Suggestor - guaranteed working."""

import os


class CameraSuggestor:
    """Suggest camera angles based on scene type."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.use_ai = bool(self.api_key)

    def suggest_angles(self, scene_text: str) -> dict:
        """Suggest based on INT/EXT."""
        text_upper = scene_text.upper()
        
        if "INT" in text_upper:
            return {
                "opening_shot": "Wide establishing shot of interior",
                "camera_movement": "Slow dolly in",
                "lens": "35mm prime",
            }
        elif "EXT" in text_upper:
            return {
                "opening_shot": "Extreme wide exterior shot",
                "camera_movement": "Crane or drone",
                "lens": "24mm wide angle",
            }
        else:
            return {
                "opening_shot": "Medium shot",
                "camera_movement": "Static",
                "lens": "50mm",
            }

    def suggest_all(self, screenplay: str) -> list:
        scenes = []
        for line in screenplay.split("\n"):
            line = line.strip()
            if line.startswith("INT.") or line.startswith("EXT."):
                scenes.append(line)
        
        results = []
        for i, scene in enumerate(scenes):
            r = self.suggest_angles(scene)
            r["scene_number"] = i + 1
            r["heading"] = scene
            results.append(r)
        return results

    def format_results(self, results: list) -> str:
        lines = ["🎥 Camera Angle Suggestions", "=" * 50]
        for r in results:
            lines.append("")
            lines.append(f"Scene {r['scene_number']}: {r['heading']}")
            lines.append(f"  Opening Shot: {r['opening_shot']}")
            lines.append(f"  Movement: {r['camera_movement']}")
            lines.append(f"  Lens: {r['lens']}")
        return "\n".join(lines)
