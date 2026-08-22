"""Continuity Tracker - يتتبع العناصر عبر المشاهد ويكتشف أخطاء الاستمرارية."""

import os


class ContinuityTracker:
    """Track props, wardrobe, and characters across scenes."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.use_ai = True
        else:
            self.use_ai = False

    def track_continuity(self, production_data: dict) -> list:
        """Find potential continuity issues."""
        issues = []
        
        # تتبع الدعائم
        props = production_data.get("props", [])
        scenes = production_data.get("scenes", [])
        wardrobe = production_data.get("wardrobe", [])
        characters = production_data.get("characters", [])
        
        # بسيط: نفترض أن كل عنصر يجب أن يظهر في أكثر من مشهد إذا تكرر
        # نتحقق من العناصر التي تظهر مرة واحدة فقط (احتمال خطأ)
        for prop in props:
            count = sum(1 for scene in scenes if prop.lower() in str(scene.get("heading", "")).lower())
            if count <= 1:
                issues.append({
                    "type": "Prop",
                    "item": prop,
                    "issue": "Appears in only one scene - verify continuity"
                })
        
        for item in wardrobe:
            count = sum(1 for scene in scenes if item.lower() in str(scene.get("heading", "")).lower())
            if count <= 1:
                issues.append({
                    "type": "Wardrobe",
                    "item": item,
                    "issue": "Appears in only one scene - verify continuity"
                })
        
        return issues

    def generate_report(self, production_data: dict) -> str:
        """Generate continuity report."""
        issues = self.track_continuity(production_data)
        
        lines = ["🔍 Continuity Report", "=" * 50]
        
        if not issues:
            lines.append("✅ No potential continuity issues detected.")
        else:
            for issue in issues:
                lines.append(f"\n⚠️ {issue['type']}: {issue['item']}")
                lines.append(f"   {issue['issue']}")
        
        lines.append("\nNote: This is a heuristic check. Review manually for accuracy.")
        return "\n".join(lines)
