"""Production Budget Estimator - يحسب التكلفة التقريبية للإنتاج."""

class BudgetEstimator:
    """Estimate production budget based on screenplay analysis."""

    def __init__(self):
        # تكاليف تقديرية بالدولار
        self.costs = {
            "scene": 5000,      # تكلفة تصوير مشهد
            "character": 2000,  # تكلفة ممثل
            "prop": 500,        # تكلفة دعامة
            "wardrobe": 1000,   # تكلفة ملابس
            "sound": 300,       # تكلفة صوت
            "lighting": 800,    # تكلفة إضاءة
            "location": 3000,   # تكلفة موقع
        }

    def estimate_budget(self, production_data: dict) -> dict:
        """Calculate estimated budget from production data."""
        breakdown = {}
        total = 0
        
        # المشاهد
        scene_count = len(production_data.get("scenes", []))
        scene_cost = scene_count * self.costs["scene"]
        breakdown["Scenes"] = {"count": scene_count, "cost": scene_cost}
        total += scene_cost
        
        # الشخصيات
        char_count = len(production_data.get("characters", []))
        char_cost = char_count * self.costs["character"]
        breakdown["Characters"] = {"count": char_count, "cost": char_cost}
        total += char_cost
        
        # الدعائم
        prop_count = len(production_data.get("props", []))
        prop_cost = prop_count * self.costs["prop"]
        breakdown["Props"] = {"count": prop_count, "cost": prop_cost}
        total += prop_cost
        
        # الملابس
        wardrobe_count = len(production_data.get("wardrobe", []))
        wardrobe_cost = wardrobe_count * self.costs["wardrobe"]
        breakdown["Wardrobe"] = {"count": wardrobe_count, "cost": wardrobe_cost}
        total += wardrobe_cost
        
        # الصوت
        sound_count = len(production_data.get("sounds", []))
        sound_cost = sound_count * self.costs["sound"]
        breakdown["Sound"] = {"count": sound_count, "cost": sound_cost}
        total += sound_cost
        
        # الإضاءة
        lighting_count = len(production_data.get("lighting", []))
        lighting_cost = lighting_count * self.costs["lighting"]
        breakdown["Lighting"] = {"count": lighting_count, "cost": lighting_cost}
        total += lighting_cost
        
        return {
            "breakdown": breakdown,
            "total_estimated_budget": total,
            "currency": "USD"
        }

    def format_budget(self, estimate: dict) -> str:
        """Format budget as readable text."""
        lines = []
        lines.append("💰 Estimated Production Budget")
        lines.append("=" * 40)
        
        for category, data in estimate["breakdown"].items():
            lines.append(f"{category}: ${data['cost']:,} ({data['count']} items)")
        
        lines.append("=" * 40)
        lines.append(f"Total: ${estimate['total_estimated_budget']:,}")
        
        return "\n".join(lines)
