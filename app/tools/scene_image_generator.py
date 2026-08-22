"""AI Scene Image Generator - uses Google GenAI SDK."""

import os
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from google import genai


class SceneImageGenerator:
    """Generate cinematic images from screenplay scenes using Gemini."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.use_ai = False
            self.client = None

    def generate_scene_image(self, scene_heading: str) -> Image:
        """Generate cinematic image for a scene, with fallback."""
        if self.use_ai:
            try:
                prompt = f"Create a cinematic film storyboard image for this scene: {scene_heading}"
                response = self.client.models.generate_content(
                    model="gemini-3-pro-image",
                    contents=prompt,
                )
                if hasattr(response, 'images') and response.images:
                    return response.images[0]
            except Exception:
                pass
        return self._generate_simple_image(scene_heading)

    def _generate_simple_image(self, scene_heading: str) -> Image:
        """Generate simple visual representation."""
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        bg_color = "#87CEEB" if "NIGHT" not in scene_heading.upper() else "#1a1a2e"
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        text_color = "black" if "NIGHT" not in scene_heading.upper() else "white"
        ax.text(5, 5.2, "SCENE", fontsize=20, ha='center', fontweight='bold', color=text_color)
        ax.text(5, 4.5, scene_heading, fontsize=14, ha='center', color=text_color)
        loc = "INTERIOR" if "INT" in scene_heading.upper() else "EXTERIOR"
        ax.add_patch(patches.Rectangle((2, 1.5), 6, 2.5, fill=True, color='#D2B48C'))
        ax.text(5, 2.75, loc, fontsize=16, ha='center', color='white', fontweight='bold')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, facecolor=bg_color)
        buf.seek(0)
        return Image.open(buf)

    def generate_all_scenes(self, screenplay: str) -> list:
        scenes = []
        for line in screenplay.split("\n"):
            line = line.strip()
            if line.startswith("INT.") or line.startswith("EXT."):
                scenes.append(line)
        results = []
        for i, scene in enumerate(scenes):
            image = self.generate_scene_image(scene)
            results.append({"scene_number": i+1, "heading": scene, "image": image, "success": image is not None})
        return results
