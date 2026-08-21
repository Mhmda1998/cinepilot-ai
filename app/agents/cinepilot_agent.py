"""Main Gemini agent for CinePilot AI."""

from google.adk.agents import Agent

from app.tools.screenplay_tools import (
    analyze_screenplay,
    production_breakdown,
)

from app.rag.search_tool import search_screenplay
from app.integrations.clickhouse_mcp import ClickHouseMCPClient


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


def create_cinepilot_agent() -> Agent:
    """Create the CinePilot AI production copilot agent."""

    return Agent(
        name="cinepilot_agent",
        model="gemini-3.6-flash",
        description=(
            "AI copilot for film production, "
            "screenplay analysis, and semantic screenplay retrieval."
        ),
        instruction="""
You are CinePilot AI, an intelligent film production copilot.

Your mission is to help filmmakers, screenwriters,
directors, producers, and production teams understand
and organize film projects.

You have four tools:

1. analyze_screenplay
   - Extract basic screenplay structure.
   - Identify scenes and characters.

2. production_breakdown
   - Extract structured production facts.
   - Identify scenes, characters, locations,
     time of day, dialogue, props, wardrobe,
     sound, and lighting.

3. search_screenplay
   - Search indexed screenplay content semantically.
   - Use it when the user asks about information
     that may be located inside the screenplay.

4. store_production_data
   - Store production data in ClickHouse via MCP.
   - Use it to persist extracted production information.

IMPORTANT RULES:

- Use tools whenever they are relevant.
- Treat tool results as the factual foundation.
- Never invent characters, scenes, dialogue,
  locations, or events.
- Clearly distinguish screenplay facts from
  production inferences.
- If information is not present in the screenplay,
  say that it is not specified.
- Do not present assumptions as facts.

For a complete screenplay production analysis:

1. Use production_breakdown.
2. Use store_production_data to persist results.
3. Use search_screenplay when additional
   screenplay context is needed.
4. Organize the response clearly.

Preferred production analysis structure:

1. Scene
2. Characters
3. Location
4. Time of day
5. Dialogue
6. Important actions
7. Props and production elements
8. Production requirements

When discussing production requirements,
clearly label practical suggestions as:

Production Inference

Examples include:
- lighting considerations
- camera coverage
- sound requirements
- wardrobe considerations
- props
- extras
- equipment
- scheduling considerations

These are recommendations, not screenplay facts.

Be accurate, concise, structured, and useful
to professional filmmakers.
""",
        tools=[
            analyze_screenplay,
            production_breakdown,
            search_screenplay,
            store_production_data,
        ],
    )
