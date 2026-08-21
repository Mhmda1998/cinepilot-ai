

import sqlite3
import json
from typing import Any


class SQLiteStorage:
    """Real local storage that works immediately."""

    def __init__(self, db_path: str = "production.db"):
        self.db_path = db_path
        self.conn = None
        self._create_tables()

    def _create_tables(self):
        """Create tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                heading TEXT,
                location TEXT,
                time_of_day TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS props (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wardrobe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lighting (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        self.conn.commit()

    def store_production_data(self, data: dict) -> bool:
        """Store production data in SQLite."""
        cursor = self.conn.cursor()
        
        # Scenes
        for scene in data.get("scenes", []):
            heading = scene.get("heading", scene.get("location", "")) if isinstance(scene, dict) else str(scene)
            location = scene.get("location", "") if isinstance(scene, dict) else ""
            time_of_day = scene.get("time", scene.get("time_of_day", "")) if isinstance(scene, dict) else ""
            cursor.execute(
                "INSERT OR IGNORE INTO scenes (heading, location, time_of_day) VALUES (?, ?, ?)",
                (heading, location, time_of_day)
            )
        
        # Characters
        for char in data.get("characters", []):
            cursor.execute("INSERT OR IGNORE INTO characters (name) VALUES (?)", (char,))
        
        # Props
        for prop in data.get("props", []):
            cursor.execute("INSERT OR IGNORE INTO props (name) VALUES (?)", (prop,))
        
        # Wardrobe
        for item in data.get("wardrobe", []):
            cursor.execute("INSERT OR IGNORE INTO wardrobe (name) VALUES (?)", (item,))
        
        # Sounds
        for sound in data.get("sounds", []):
            cursor.execute("INSERT OR IGNORE INTO sounds (name) VALUES (?)", (sound,))
        
        # Lighting
        for light in data.get("lighting", []):
            cursor.execute("INSERT OR IGNORE INTO lighting (name) VALUES (?)", (light,))
        
        self.conn.commit()
        return True

    def get_all_data(self) -> dict:
        """Retrieve all stored data."""
        cursor = self.conn.cursor()
        
        result = {
            "scenes": cursor.execute("SELECT heading FROM scenes").fetchall(),
            "characters": [r[0] for r in cursor.execute("SELECT name FROM characters").fetchall()],
            "props": [r[0] for r in cursor.execute("SELECT name FROM props").fetchall()],
            "wardrobe": [r[0] for r in cursor.execute("SELECT name FROM wardrobe").fetchall()],
            "sounds": [r[0] for r in cursor.execute("SELECT name FROM sounds").fetchall()],
            "lighting": [r[0] for r in cursor.execute("SELECT name FROM lighting").fetchall()],
        }
        
        return result

    def close(self):
        """Close connection."""
        if self.conn:
            self.conn.close()
