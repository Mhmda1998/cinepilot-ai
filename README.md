
# CinePilot AI
> AI-powered screenplay analysis and production copilot built with Gemini.

CinePilot transforms screenplay text into structured production intelligence
using deterministic screenplay analysis tools, AI agents, and semantic search.

---

## What CinePilot Does

CinePilot analyzes screenplay text and extracts production-relevant
information for filmmakers, producers, directors, and production teams.

### Screenplay Intelligence
- Scene detection
- Character extraction
- Location extraction
- Time-of-day detection
- Dialogue extraction
- Action extraction
- Props extraction
- Wardrobe extraction
- Sound extraction
- Lighting extraction

### Production Intelligence

CinePilot separates:
- **Screenplay Facts** - information explicitly present in the screenplay.
- **Production Inferences** - practical recommendations generated for planning.

This separation helps distinguish information explicitly written in the
screenplay from AI-generated production recommendations.

---

## Architecture

```text
                         +---------------------+
                         |      Screenplay     |
                         +----------+----------+
                                    |
                                    v
                         +---------------------+
                         | Screenplay Analysis |
                         +----------+----------+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
          +---------------------+        +---------------------+
          | Production Engine   |        | Semantic RAG        |
          |                     |        |                     |
          | Scenes              |        | Chunking            |
          | Characters          |        | Embeddings          |
          | Locations           |        | Retrieval           |
          | Time                |        | Semantic Search     |
          | Dialogue            |        |                     |
          | Actions             |        +----------+----------+
          | Props               |                   |
          | Wardrobe            |                   |
          | Sound               |                   |
          | Lighting            |                   |
          +----------+----------+                   |
                     |                              |
                     +--------------+---------------+
                                    |
                                    v
                         +---------------------+
                         |   CinePilot Agent   |
                         |                     |
                         | Gemini              |
                         | Tool Calling        |
                         | Production Analysis |
                         +----------+----------+
                                    |
                                    v
                         +---------------------+
                         | Production Report   |
                         +---------------------+
```

---

CinePilot Agent

The main CinePilot agent is:

· Name: cinepilot_agent
· Model: gemini-3.6-flash

Available Tools

· analyze_screenplay
· production_breakdown
· search_screenplay

The agent uses production_breakdown as the primary production analysis
tool and can use search_screenplay when additional screenplay context
is required.

The agent has successfully passed an integration test using the production
workflow and tool calling.

---

Production Breakdown

CinePilot extracts structured production information including:

· Scenes
· Characters
· Locations
· Time of Day
· Dialogue
· Actions
· Props
· Wardrobe
· Sound
· Lighting

Example

```text
Scenes:
2

Characters:
JOHN
SARAH

Location:
COFFEE SHOP

Time:
DAY
NIGHT

Actions:
- John enters the coffee shop carrying a black backpack.
- He picks up a coffee cup from the table.
- John opens the door and leaves the coffee shop.

Props:
- black backpack
- coffee cup
- door

Wardrobe:
- black jacket
- red dress

Sound:
- phone
- door
- footsteps
- car engine

Lighting:
- bright lights
- neon light
```

Example Screenplay

```text
INT. COFFEE SHOP - DAY
John enters carrying a black backpack
and wearing a black jacket.
A phone rings.

JOHN
Sarah? I didn't expect to see you here.

SARAH
Neither did I.

John opens the door.

EXT. COFFEE SHOP - NIGHT
A neon light glows above the door.
A car engine starts.
John leaves wearing the same black jacket.
```

CinePilot can extract production elements from this screenplay and organize
them into structured production data.

The agent can then provide production-oriented recommendations while clearly
separating screenplay facts from production inferences.

---

Production Components

The production engine currently supports:

```text
Screenplay Analysis
        |
        +-- Scenes
        +-- Characters
        +-- Locations
        +-- Time of Day
        +-- Dialogue
        +-- Actions
        +-- Props
        +-- Wardrobe
        +-- Sound
        +-- Lighting
```

All major production extraction components have been individually tested.

---

Testing

CinePilot has been tested through component tests, regression tests,
production integration tests, and agent integration tests.

Production Engine

```text
Screenplay Analysis       PASS
Scene Extraction          PASS
Character Extraction      PASS
Location Extraction       PASS
Time Extraction           PASS
Dialogue Extraction       PASS
Action Extraction         PASS
Props Extraction          PASS
Wardrobe Extraction       PASS
Sound Extraction          PASS
Lighting Extraction       PASS
```

Production Integration

```text
Production Breakdown      PASS
Actions                   PASS
Props                     PASS
Wardrobe                  PASS
Sound                     PASS
Lighting                  PASS
Dialogue                  PASS
```

Regression Tests

Original screenplay regression tests have passed for:

```text
Original Screenplay       PASS
Props Regression          PASS
Wardrobe Regression       PASS
Sound Regression          PASS
```

These regression tests help ensure that adding new production extraction
features does not break the original screenplay analysis behavior.

End-to-End Production Test

```text
1. Screenplay Analysis       PASS
2. Production Breakdown      PASS
3. Actions                   PASS
4. Props                     PASS
5. Wardrobe                  PASS
6. Sound                     PASS
7. Lighting                  PASS
8. Dialogue                  PASS

Result:

CINEPILOT PRODUCTION ENGINE
END-TO-END PASSED
```

---

Agent Integration Test

The CinePilot agent has also passed an integration test.

```text
Gemini Agent              PASS
Tool Calling              PASS
Production Breakdown      PASS
Fact / Inference Split    PASS
End-to-End Agent Test     PASS
```

The successful agent test demonstrated that CinePilot can process a screenplay
and return structured screenplay facts together with production-oriented
inferences.

---

Retrieval-Augmented Generation

CinePilot includes a semantic retrieval pipeline:

```text
Screenplay
    |
    v
Chunking
    |
    v
Gemini Embeddings
    |
    v
Vector Retrieval
    |
    v
Semantic Search
    |
    v
CinePilot Agent
```

The RAG system is implemented through:

· chunker.py
· embeddings.py
· retriever.py
· search_tool.py

RAG Status

The RAG implementation is present and integrated with the project.

During a final RAG test, the Gemini Embeddings API returned:

```text
429 RESOURCE_EXHAUSTED
```

The reported quota was:

```text
embed_content_free_tier_requests
```

This means the test was blocked by the Gemini Embeddings API quota rather
than by a detected failure in the CinePilot RAG implementation.

Repeated embedding requests may therefore require additional quota,
waiting for the quota window to reset, or an appropriate Gemini API plan.

---

Project Structure

```text
cinepilot-ai/
|
+-- app/
|   |
|   +-- agents/
|   |   +-- cinepilot_agent.py
|   |
|   +-- rag/
|   |   +-- chunker.py
|   |   +-- embeddings.py
|   |   +-- retriever.py
|   |   +-- search_tool.py
|   |
|   +-- tools/
|       +-- screenplay_tools.py
|
+-- tests/
|
+-- README.md
+-- requirements.txt
```

---

Installation

Clone the repository:

```bash
git clone https://github.com/Mhmda1998/cinepilot-ai.git
cd cinepilot-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

Environment Variables

CinePilot uses a Gemini API key for Gemini-powered functionality.

```text
GEMINI_API_KEY
```

For GitHub development environments, authentication can be provided through:

```text
GITHUB_TOKEN
```

Never commit API keys, access tokens, or other secrets to the repository.

---

Design Goals

1. Structured Screenplay Understanding
   Transform screenplay text into structured production information.
2. Grounded Analysis
   Prefer information explicitly present in the screenplay.
3. Production Intelligence
   Generate useful production-oriented recommendations.
4. Fact / Inference Separation
   Clearly distinguish screenplay facts from AI-generated production
   recommendations.
5. Agentic Workflow
   Combine deterministic screenplay tools, semantic retrieval, and Gemini
   reasoning into a unified production copilot.

---

Current Status

```text
Core Production Engine       COMPLETE
Screenplay Analysis          COMPLETE
Scene Extraction             COMPLETE
Character Extraction         COMPLETE
Location Extraction          COMPLETE
Time Extraction              COMPLETE
Dialogue Extraction          COMPLETE
Action Extraction            COMPLETE
Props Extraction             COMPLETE
Wardrobe Extraction          COMPLETE
Sound Extraction             COMPLETE
Lighting Extraction          COMPLETE
Production Breakdown         COMPLETE
Gemini Agent                 COMPLETE
Tool Calling                 TESTED
Agent Integration            PASSING
Regression Tests             PASSING
Semantic RAG                 IMPLEMENTED
GitHub Repository            ACTIVE
Final Demo                   IN PROGRESS
```

---

What Has Been Verified

The following production workflow has been successfully verified:

```text
Screenplay
    |
    v
Screenplay Analysis
    |
    v
Production Breakdown
    |
    +-- Actions
    +-- Props
    +-- Wardrobe
    +-- Sound
    +-- Lighting
    +-- Dialogue
    |
    v
CinePilot Agent
    |
    v
Production Analysis
```

The production engine successfully passed the complete end-to-end production
test.

The CinePilot agent also successfully passed its integration test.

---

Project Vision

CinePilot is designed to become an intelligent production copilot that helps
film teams move from screenplay understanding to practical production
planning.

Instead of simply summarizing a screenplay, CinePilot aims to extract
actionable production intelligence and help teams understand:

· What is explicitly written.
· What production elements are required.
· What can reasonably be inferred for planning.
· What additional screenplay context may be relevant.

The long-term goal is to bridge the gap between screenplay text and
real-world production planning.

---

Roadmap

Future development can include:

· Advanced scene-level production reports
· Better continuity tracking
· Character appearance tracking
· Location-based breakdowns
· Advanced wardrobe continuity
· Advanced sound design planning
· Advanced lighting planning
· Production scheduling assistance
· Shot and coverage recommendations
· Improved RAG retrieval
· Persistent screenplay projects
· Exportable production reports
· Production dashboard
· Multi-agent production workflows

---

License

See the repository license for usage and distribution terms.

```


---

## ClickHouse MCP Integration

CinePilot integrates with ClickHouse through Model Context Protocol (MCP) for storing and querying production data.

### Files

- `app/integrations/clickhouse_mcp.py` - ClickHouse MCP client
- `config/clickhouse.example.env` - Configuration template
- `tests/test_clickhouse.py` - ClickHouse integration tests
- `tests/test_agent_clickhouse.py` - Agent-ClickHouse integration tests

### Configuration

Copy the example config and fill in your credentials:

```bash
cp config/clickhouse.example.env .env
```

### Agent Tool

The CinePilot agent includes `store_production_data` as a tool:

```python
from app.agents.cinepilot_agent import create_cinepilot_agent

agent = create_cinepilot_agent()
# Agent has 4 tools:
# 1. analyze_screenplay
# 2. production_breakdown
# 3. search_screenplay
# 4. store_production_data
```

### Workflow

```
CinePilot Agent
      ↓
Tool Calling
      ↓
ClickHouse MCP
      ↓
ClickHouse Database
      ↓
Result
```
