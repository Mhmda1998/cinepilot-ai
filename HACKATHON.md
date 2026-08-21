# CinePilot AI - Hackathon Submission

## Event: Agentic Cinema Hackathon

## Project Overview

CinePilot AI is an AI-powered screenplay analysis and production copilot that transforms screenplay text into structured production intelligence.

## Requirements Checklist

| Requirement | Status |
|-------------|--------|
| Gemini-powered | YES |
| Google Cloud ADK | YES |
| Partner Integration (ClickHouse) | YES |
| Entertainment Focus | YES |
| Production-ready | YES |

## Partner Integration: ClickHouse

CinePilot integrates ClickHouse through MCP for storing production data.

### Files:
- app/integrations/clickhouse_mcp.py
- config/clickhouse.example.env
- tests/test_clickhouse.py
- tests/test_agent_clickhouse.py

### Agent Tool:
- store_production_data

## Production Features

- Scenes
- Characters
- Locations
- Props
- Wardrobe
- Sound
- Lighting

## Testing

- Component tests: PASS
- Regression tests: PASS
- End-to-end test: PASS
- ClickHouse tests: PASS

## Quick Start

git clone https://github.com/Mhmda1998/cinepilot-ai.git
cd cinepilot-ai
pip install -r requirements.txt

## Environment Variables

- GEMINI_API_KEY
- CLICKHOUSE_HOST
- CLICKHOUSE_PORT
- CLICKHOUSE_USER
- CLICKHOUSE_DATABASE
