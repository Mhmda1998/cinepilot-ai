"""Auto Shooting Schedule - يولد جدول تصوير من تحليل السيناريو."""

import os


class ShootingSchedule:
    """Generate shooting schedule from screenplay scenes."""

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

    def generate_schedule(self, scenes: list) -> list:
        """Group scenes into shooting days."""
        if not scenes:
            return []

        # تجميع المشاهد حسب الموقع والوقت
        groups = {}
        for scene in scenes:
            location = scene.get("location", "Unknown")
            time_of_day = scene.get("time_of_day", scene.get("time", "Unknown"))
            key = f"{location} - {time_of_day}"
            if key not in groups:
                groups[key] = []
            groups[key].append(scene)

        schedule = []
        day_num = 1
        for group_key, group_scenes in groups.items():
            schedule.append({
                "day": day_num,
                "location": group_key.split(" - ")[0],
                "time_of_day": group_key.split(" - ")[1],
                "scene_count": len(group_scenes),
                "scenes": group_scenes
            })
            day_num += 1

        return schedule

    def format_schedule(self, schedule: list) -> str:
        """Format schedule as readable text."""
        lines = ["📅 Shooting Schedule", "=" * 50]
        for entry in schedule:
            lines.append(f"\nDay {entry['day']}:")
            lines.append(f"  Location: {entry['location']}")
            lines.append(f"  Time: {entry['time_of_day']}")
            lines.append(f"  Scenes: {entry['scene_count']}")
        lines.append("\nNote: This is an automatic suggestion based on scene locations and times.")
        return "\n".join(lines)
