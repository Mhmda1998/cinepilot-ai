"""AI Storyboard Generator - يولد صوراً حقيقية من السيناريو."""

import os
import io
import matplotlib.pyplot as plt
from PIL import Image


class AIStoryboardGenerator:
    """Generate storyboard images from screenplay.
    
    Works in two modes:
    - With GEMINI_API_KEY: Uses Gemini AI to generate real images
    - Without key: Uses simple visual representation
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        
        if self.api_key:
            self.use_ai = True
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-3-pro-image")
        else:
            self.use_ai = False
            self.model = None

    def generate_storyboard(self, screenplay: str) -> list:
        """Generate storyboard from screenplay."""
        scenes = self._extract_scenes(screenplay)
        storyboard = []
        
        for i, scene in enumerate(scenes):
            if self.use_ai:
                image = self._generate_ai_image(scene)
            else:
                image = self._generate_simple_image(scene, i+1)
            
            storyboard.append({
                "scene_number": i+1,
                "heading": scene,
                "image": image,
                "ai_generated": self.use_ai
            })
        
        return storyboard

    def _extract_scenes(self, text: str) -> list:
        """Extract scene headings."""
        scenes = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("INT.") or line.startswith("EXT."):
                scenes.append(line)
        return scenes

    def _generate_ai_image(self, scene: str) -> Image:
        """Generate real AI image using Gemini."""
        try:
            prompt = f"Storyboard image for film scene: {scene}. Cinematic style, film production storyboard."
            response = self.model.generate_content(prompt)
            
            # استخراج الصورة من الاستجابة
            if hasattr(response, 'images') and response.images:
                return response.images[0]
            
            # بديل: استخدام النص كوصف
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, scene, ha='center', fontsize=14)
            ax.axis('off')
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            return Image.open(buf)
            
        except Exception as e:
            return self._generate_simple_image(scene, 0)

    def _generate_simple_image(self, scene: str, number: int) -> Image:
        """Generate simple visual representation."""
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        ax.text(5, 3.5, f"SCENE {number}", fontsize=24, ha='center', color='#00d2ff', fontweight='bold')
        ax.text(5, 2.5, scene, fontsize=14, ha='center', color='white')
        ax.text(5, 1.5, "(Add GEMINI_API_KEY for AI images)", fontsize=10, ha='center', color='#7a7a9a')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor='#1a1a2e')
        buf.seek(0)
        return Image.open(buf)

    def save_storyboard(self, storyboard: list, output_path: str = "storyboard.png"):
        """Save storyboard as single image."""
        if not storyboard:
            return None
        
        fig, axes = plt.subplots(1, len(storyboard), figsize=(4*len(storyboard), 4))
        if len(storyboard) == 1:
            axes = [axes]
        
        for ax, scene in zip(axes, storyboard):
            ax.imshow(scene["image"])
            ax.axis('off')
            ax.set_title(f"Scene {scene['scene_number']}", fontsize=12)
        
        plt.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
