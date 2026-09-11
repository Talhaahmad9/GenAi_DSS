<div align="center">

# 🎭 Multi-Agent Narrative Simulation Engine

### Autonomous Agents. Dynamic Actions. Persistent World State.

[![Python](https://img.shields.io/badge/Python-3.11%2B-00ff41?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-00ff41?style=for-the-badge&logo=graphql&logoColor=black)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-00ff41?style=for-the-badge&logo=google&logoColor=black)](https://ai.google.dev)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-00ff41?style=for-the-badge&logo=nextdotjs&logoColor=black)](https://nextjs.org)

**Team Midnight Sons**  
**1st Place — IBA Hackfest × Datathon 2026**

</div>

---

## Overview

The **Multi-Agent Narrative Simulation Engine** is an agent-based storytelling system built for **IBA Hackfest × Datathon 2026**.

Instead of generating an entire story in a single LLM response, the system creates a persistent simulated world where autonomous agents make decisions, perform actions, interact with other characters, maintain memory, and gradually progress toward the resolution of a hidden mystery.

The simulation is orchestrated with **LangGraph**, while **Pydantic** keeps agent outputs and world state structured and predictable.

### What the system does

- Runs multiple autonomous character agents in the same world
- Uses a director/orchestrator agent to coordinate narrative progression
- Maintains persistent character and world state across turns
- Tracks ownership and movement of important entities
- Validates structured agent outputs before applying state changes
- Generates a multi-turn narrative rather than a single-shot story
- Logs agent activity for debugging and evaluation
- Provides a Next.js frontend for simulation control and inspection

---

## Key Features

### Multi-Agent Orchestration

Multiple autonomous agents operate inside the same simulated world.

Each agent can:

- inspect the current world state
- react to previous events
- use relevant character memory
- select an action
- interact with other characters
- affect tracked entities
- influence the direction of the story

A central director agent coordinates the simulation and helps keep the narrative moving toward a meaningful resolution.

### Persistent World State

The simulation keeps state across turns instead of treating every LLM call independently.

Tracked state includes:

- character information
- character memory
- previous actions
- narrative events
- entity ownership
- global story state
- simulation progress

Pydantic models are used to validate and structure this information.

### Entity Ownership Registry

The engine maintains a global registry for important objects and entities.

For example, if a wallet belongs to one character, that ownership remains tracked across later turns instead of allowing the object to appear inconsistently with another character.

This helps reduce continuity errors in long-running simulations.

### Structured Agent Decisions

Agent responses are processed as structured outputs rather than unrestricted free-form text.

A turn can contain information such as:

- current interpretation of the situation
- selected action
- dialogue
- affected entities
- target characters
- resulting state changes

These outputs are validated before being applied to the simulation state.

### Dynamic Narrative Progression

The story develops across multiple turns.

Characters gradually:

- discover information
- react to events
- interact with one another
- change the world state
- move toward a final mystery resolution

The generated narrative is written to:

```text
story_output.json
```

Simulation and agent logs are written to:

```text
prompts_log.json
```

### Interactive Frontend

The project includes a Next.js frontend for controlling and inspecting the simulation.

The interface supports:

- starting the simulation
- stopping the simulation
- stepping through turns
- viewing agent actions
- following the event feed
- inspecting world state
- inspecting character memory and state

---

## Architecture

```text
                 ┌──────────────────────┐
                 │      Next.js UI      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Backend Server     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   LangGraph Engine   │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Agent A  │  │ Agent B  │  │ Agent C  │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 ┌──────────────────────┐
                 │   Director Agent     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ World / Story State  │
                 │ Pydantic + Registry  │
                 └──────────────────────┘
```

---

## Project Structure

```text
GenAi_DSS/
├── backend/
│   ├── examples/                  # Story seeds and character configurations
│   ├── src/
│   │   ├── agents/               # Character and director agent logic
│   │   ├── graph/                # LangGraph workflow
│   │   ├── prompts/              # Prompt templates
│   │   ├── config.py             # LLM and system configuration
│   │   ├── schemas.py            # Pydantic models
│   │   ├── story_state.py        # World state and entity registry
│   │   └── main.py               # CLI simulation entry point
│   ├── server.py                 # Backend server for frontend communication
│   ├── story_output.json         # Generated narrative
│   ├── prompts_log.json          # Simulation and agent logs
│   └── ...
├── frontend/
│   ├── app/                      # Next.js application
│   ├── components/               # UI components
│   ├── public/                   # Static assets
│   ├── package.json
│   └── ...
├── README.md
└── ...
```

---

## Tech Stack

| Area | Technology |
|---|---|
| Backend Language | Python 3.11+ |
| Agent Framework | LangGraph / LangChain |
| LLM | Google Gemini 2.0 Flash |
| State Validation | Pydantic v2 |
| Package Manager | UV |
| Frontend | Next.js / React |
| Styling | Tailwind CSS |
| Backend Communication | API |
| Output Format | JSON |
| Approx. API Calls | ~45 per simulation |
| Typical Runtime | ~3–5 minutes |

> Runtime and API usage may vary depending on the simulation configuration and model behavior.

---

## Quick Start

### Prerequisites

Make sure you have:

- Python 3.11+
- UV
- Node.js 18+
- npm or Yarn
- Google Gemini API key

### Clone the Repository

```bash
git clone https://github.com/Talhaahmad9/GenAi_DSS.git
cd GenAi_DSS
```

---

## Backend Setup

Move into the backend directory:

```bash
cd backend
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```bash
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```

### Run the Simulation from the CLI

```bash
uv run src/main.py
```

After execution, the simulation generates:

```text
story_output.json
prompts_log.json
```

### Start the Backend Server

The frontend requires the backend server to be running:

```bash
python server.py
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:3000
```

Make sure the backend server is running before using the frontend.

---

## Simulation Flow

A simplified simulation cycle looks like this:

```text
1. Load current world state
2. Select the active agent
3. Provide relevant memory and events
4. Agent evaluates the situation
5. Agent selects an action
6. Validate the structured output
7. Apply state changes
8. Update the entity registry
9. Director evaluates narrative progress
10. Continue to the next turn
```

The process continues until the configured simulation length is reached and the narrative concludes.

---

## Generated Outputs

### Narrative Output

```text
backend/story_output.json
```

Contains the generated narrative and resulting story events.

### Simulation Logs

```text
backend/prompts_log.json
```

Contains structured logs from the simulation, useful for:

- debugging
- evaluating agent behavior
- inspecting decisions
- understanding narrative progression

---

## Key Files

| File | Purpose |
|---|---|
| `src/agents/` | Character and director agent logic |
| `src/graph/` | LangGraph orchestration |
| `src/prompts/` | Agent prompt definitions |
| `src/story_state.py` | Global story state and entity registry |
| `src/schemas.py` | Pydantic schemas and structured outputs |
| `src/config.py` | Model and system configuration |
| `server.py` | Backend server |
| `story_output.json` | Final narrative output |
| `prompts_log.json` | Simulation and debugging logs |

---

## Evaluation Goals

The system was designed around several hackathon evaluation requirements.

### Action Diversity

Agents should perform varied and meaningful actions instead of repeatedly choosing the same behavior.

### Entity Consistency

Tracked objects should maintain consistent ownership and state throughout the simulation.

### Structured Agent Output

Agent decisions are processed through structured schemas instead of relying entirely on unrestricted text generation.

### Persistent State

Events from previous turns affect later decisions and narrative progression.

### Narrative Resolution

The simulation gradually progresses toward a coherent conclusion that resolves the central mystery.

---

## Troubleshooting

### Missing Gemini API Key

Ensure this file exists:

```text
backend/.env
```

and contains:

```env
GOOGLE_API_KEY=your_actual_key
```

### Python Dependency Issues

Reinstall backend dependencies:

```bash
uv sync
```

### Frontend Dependency Issues

```bash
rm -rf node_modules package-lock.json
npm install
```

If necessary:

```bash
npm cache clean --force
```

### Port 3000 Already in Use

```bash
npx kill-port 3000
```

Then restart:

```bash
npm run dev
```

### Adjust Simulation Length

The simulation length can be configured in the story state.

Example:

```python
self.total_turns = random.randint(18, 22)
```

---

## Hackathon

### IBA Hackfest × Datathon 2026

**Result: 1st Place**

The project was developed by **Team Midnight Sons** during IBA Hackfest × Datathon 2026.

The challenge involved building an agent-based narrative system capable of:

- maintaining persistent state
- producing diverse actions
- tracking entities consistently
- coordinating multiple autonomous agents
- progressing toward a generated mystery resolution

The project combined:

- multi-agent orchestration
- LLM-based decision making
- structured state management
- entity tracking
- backend development
- frontend visualization
- simulation control

---

## Team

<div align="center">

### 🌙 Midnight Sons

**Moiz Ali Siddiqui**  
**Syed Ayaan Nadeem**  
**Talha Ahmad**

**IBA Hackfest × Datathon 2026**

</div>

---

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the backend or frontend as required.
5. Submit a pull request with a clear description of the changes.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Acknowledgments

- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Google Gemini](https://ai.google.dev)
- [Next.js](https://nextjs.org)
- IBA Karachi for hosting Hackfest × Datathon 2026

---

<div align="center">

### Built by Team Midnight Sons

For additional implementation details, see the technical documentation included in the repository.

</div>