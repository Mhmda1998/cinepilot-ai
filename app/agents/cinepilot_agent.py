"""Main Gemini agent for CinePilot AI."""

import os
from google.adk.agents import Agent

from app.tools.screenplay_tools import (
    analyze_screenplay,
    production_breakdown,
)

from app.rag.search_tool import search_screenplay
from app.integrations.clickhouse_mcp import ClickHouseMCPClient
from app.tools.production_bible import ProductionBible


def store_production_data(production_data: dict) -> dict:
    """Store production data in ClickHouse via MCP."""
    client = ClickHouseMCPClient()
    
    if client.connect():
        result = client.store_production_data(production_data)
        client.close()
        return {
            "success": result,
            "message": "Data stored in ClickHouse" if result else "Storage failed",
        }
    
    return {
        "success": False,
        "message": "ClickHouse connection failed",
    }


def generate_production_bible(screenplay: str) -> str:
    """Generate full production report from screenplay."""
    bible = ProductionBible()
    report = bible.generate_full_report(screenplay)
    return report


def create_cinepilot_agent() -> Agent:
    """Create the CinePilot AI production copilot agent."""

    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        print("⚠️ GEMINI_API_KEY not set, agent will run without Gemini model.")
    
    return Agent(
        name="cinepilot_agent",
        model="gemini-3.6-flash" if api_key else None,
        description=(
            "AI copilot for film production, screenplay analysis, "
            "and semantic screenplay retrieval."
        ),
        instruction="""
You are CinePilot AI, an intelligent film production copilot.

You have five tools:

1. analyze_screenplay
   - Extract basic screenplay structure.
   - Identify scenes and characters.

2. production_breakdown
   - Extract structured production facts.
   - Identify scenes, characters, locations, time of day,
     dialogue, props, wardrobe, sound, and lighting.

3. search_screenplay
   - Search indexed screenplay content semantically.

4. store_production_data
   - Store production data in ClickHouse via MCP.

5. generate_production_bible
   - Generate a complete production report that includes:
     analysis, breakdown, coverage, mood, dialogue emotion,
     camera angles, shooting schedule, budget, casting,
     and continuity report.

Use generate_production_bible when the user asks for a complete
production report, a production bible, or a full analysis.

Always use tools when relevant. Treat tool results as the factual
foundation. Never invent information. Clearly distinguish screenplay
facts from production inferences.

For a complete screenplay production analysis:
1. Use generate_production_bible.
2. Use store_production_data to persist results if needed.
3. Organize the response clearly.

Be accurate, concise, structured, and useful to professional filmmakers.
""",
        tools=[
            analyze_screenplay,
            production_breakdown,
            search_screenplay,
            store_production_data,
            generate_production_bible,
        ],
    )
