"""AI Scene Image Generator - يحول المشاهد إلى صور سينمائية حقيقية."""

import os
import io
from PIL import Image


class SceneImageGenerator:
    """Generate cinematic images from screenplay scenes using Gemini."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        
        if self.api_key:
            self.use_ai = True
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            # استخدام نموذج توليد الصور
            self.model = genai.GenerativeModel("gemini-3-pro-image")
        else:
            self.use_ai = False
            self.model = None

    def generate_scene_image(self, scene_heading: str) -> Image:
        """Generate cinematic image for a scene."""
        prompt = f"""
        Create a cinematic film storyboard image for this scene:
        {scene_heading}
        
        Style: Professional film storyboard, cinematic lighting, detailed.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # استخراج الصورة من الاستجابة
            if hasattr(response, 'images') and response.images:
                return response.images[0]
            
            # إذا لا توجد صورة مباشرة، نرجع None
            return None
            
        except Exception as e:
            print(f"Warning: {e}")
            return None

    def generate_all_scenes(self, screenplay: str) -> list:
        """Generate images for all scenes in screenplay."""
        scenes = self._extract_scenes(screenplay)
        results = []
        
        for i, scene in enumerate(scenes):
            print(f"Generating image for scene {i+1}...")
            image = self.generate_scene_image(scene)
            results.append({
                "scene_number": i+1,
                "heading": scene,
                "image": image,
                "success": image is not None
            })
        
        return results

    def _extract_scenes(self, text: str) -> list:
        """Extract scene headings from screenplay."""
        scenes = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("INT.") or line.startswith("EXT."):
                scenes.append(line)
        return scenes
