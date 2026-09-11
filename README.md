<div align="center">

# 🎭 Multi-Agent Narrative Simulation Engine

### Autonomous agents, evolving world state, and emergent narrative generation

[![Python](https://img.shields.io/badge/Python-3.11%2B-00ff41?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-00ff41?style=for-the-badge&logo=graphql&logoColor=black)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-00ff41?style=for-the-badge&logo=google&logoColor=black)](https://ai.google.dev)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-00ff41?style=for-the-badge&logo=nextdotjs&logoColor=black)](https://nextjs.org)

**Team Midnight Sons**  
**1st Place — IBA Hackfest × Datathon 2026**

</div>

---

## Overview

This project is a multi-agent narrative simulation engine built for **IBA Hackfest × Datathon 2026**.

The system simulates a dynamic fictional world in which autonomous characters make decisions, perform actions, interact with other agents, maintain state, and collectively progress toward the resolution of a hidden mystery.

Instead of generating a story in a single LLM response, the project models the narrative as a sequence of stateful agent interactions coordinated through **LangGraph**.

The system includes:

- autonomous character agents
- a director/orchestrator agent
- persistent world and character state
- entity ownership tracking
- structured agent decisions
- dynamic action generation
- narrative progression across multiple turns
- generated event logs
- a frontend dashboard for simulation control and inspection

---

## Key Features

### Multi-Agent Orchestration

Multiple agents operate inside the same simulated world.

Each agent can:

- inspect the current world state
- react to previous events
- decide what action to take
- interact with other characters
- update its own memory/state
- influence the direction of the story

A central director agent coordinates the simulation and ensures that actions remain consistent with the evolving narrative.

### Persistent World State

The simulation maintains structured state across turns instead of treating every LLM call independently.

State includes:

- character information
- memories
- current narrative events
- tracked entities
- entity ownership
- previous actions
- global simulation state

Pydantic models are used to keep the state structured and predictable.

### Entity Ownership Registry

The engine maintains a global entity registry to prevent inconsistent ownership of important objects.

For example, if a wallet belongs to one character, the state system tracks that ownership across future turns instead of allowing the object to randomly appear with another character.

### Dynamic Agent Decisions

Agents produce structured outputs containing information such as:

- reasoning/state interpretation
- selected action
- dialogue
- affected characters or entities

These outputs are validated before being applied to the simulation state.

### Narrative Progression

The system runs for a configurable number of turns.

Across those turns, agents gradually reveal information, react to events, and move the story toward a final resolution.

The generated result is written to:

```text
story_output.json

Agent interaction and prompt logs are written to:

prompts_log.json

Interactive Frontend

The project includes a Next.js frontend for inspecting and controlling the simulation.

The interface allows users to:

start the simulation

stop execution

progress the simulation step-by-step

inspect agent actions

view the event feed

inspect world state

inspect character information and memory



---

Architecture

┌──────────────────────┐
                 │     User / UI        │
                 │      Next.js         │
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


---

Project Structure

GenAi_DSS/
├── backend/
│   ├── examples/
│   │   └── ...                     # Story seeds and character configurations
│   │
│   ├── src/
│   │   ├── agents/
│   │   │   └── ...                 # Agent and director logic
│   │   │
│   │   ├── graph/
│   │   │   └── ...                 # LangGraph workflow
│   │   │
│   │   ├── prompts/
│   │   │   └── ...                 # Prompt templates
│   │   │
│   │   ├── config.py               # LLM and application configuration
│   │   ├── schemas.py              # Pydantic models
│   │   ├── story_state.py          # Global simulation state
│   │   └── main.py                 # CLI simulation entry point
│   │
│   ├── server.py                   # Backend API/server
│   ├── story_output.json           # Generated narrative output
│   ├── prompts_log.json            # Simulation and agent logs
│   └── ...
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── README.md
└── ...


---

Tech Stack

Area	Technology

Language	Python 3.11+
Agent Framework	LangGraph / LangChain
LLM	Google Gemini 2.0 Flash
Validation / State	Pydantic v2
Backend Package Manager	UV
Frontend	Next.js / React
Styling	Tailwind CSS
Communication	Backend API
Output	JSON
Approx. API Calls	~45 per simulation
Typical Runtime	~3–5 minutes


> Runtime and API usage can vary depending on the selected story configuration and model behavior.




---

Getting Started

Prerequisites

Make sure you have:

Python 3.11+
UV
Node.js 18+
npm
Google Gemini API key


---

Installation

Clone the repository:

git clone https://github.com/Talhaahmad9/GenAi_DSS.git
cd GenAi_DSS


---

Backend Setup

Move into the backend directory:

cd backend

Install dependencies:

uv sync

Create a .env file:

echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

Run the Simulation from CLI

uv run src/main.py

After execution, the system generates:

story_output.json
prompts_log.json

Start the Backend Server

The frontend requires the backend server to be running.

python server.py


---

Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Then open:

http://localhost:3000

Make sure the backend server is already running before using the frontend.


---

Frontend Capabilities

The dashboard allows you to:

start a simulation

pause or stop execution

step through simulation turns

view agent actions

inspect the event feed

inspect world state

inspect character state and memory



---

Generated Outputs

Story Output

backend/story_output.json

Contains the generated narrative and final sequence of story events.

Agent / Prompt Logs

backend/prompts_log.json

Contains structured logs of agent interactions and decisions during the simulation.

These logs are useful for debugging, evaluation, and understanding how the agents influenced the final outcome.


---

Core Files

File	Purpose

src/agents/	Character and director agent logic
src/story_state.py	Global world and narrative state
src/schemas.py	Pydantic models and structured outputs
src/graph/	LangGraph workflow and simulation orchestration
src/prompts/	Prompt definitions
server.py	Backend API for frontend communication
story_output.json	Final generated narrative
prompts_log.json	Agent interaction and debugging logs



---

Evaluation Goals

The project was designed around several hackathon evaluation requirements.

Action Diversity

Agents should perform a variety of meaningful actions instead of repeating the same behavior.

Entity Consistency

Tracked objects should remain consistent throughout the simulation.

For example, ownership of important entities should not randomly change between turns.

Structured Agent Decisions

Agent responses are processed as structured outputs rather than unvalidated free-form text.

Narrative Resolution

The simulation should gradually progress toward a coherent conclusion that resolves the central mystery.


---

Example Simulation Flow

A simplified simulation cycle looks like this:

1. Load current world state
2. Select active agent
3. Provide relevant memory and events
4. Agent evaluates the situation
5. Agent selects an action
6. Output is validated
7. World state is updated
8. Director evaluates narrative progress
9. Next turn begins
10. Continue until the simulation concludes


---

Troubleshooting

Missing Gemini API Key

Ensure the file exists here:

backend/.env

and contains:

GOOGLE_API_KEY=your_actual_key


---

Python Dependencies

Reinstall backend dependencies:

uv sync


---

Frontend Dependency Issues

rm -rf node_modules package-lock.json
npm install

If necessary:

npm cache clean --force


---

Port 3000 Already in Use

npx kill-port 3000

Then restart:

npm run dev


---

Adjust Simulation Length

The number of turns can be configured in the simulation state.

Example:

self.total_turns = random.randint(18, 22)


---

Hackathon

IBA Hackfest × Datathon 2026

Result: 1st Place

The project was developed by Team Midnight Sons during the hackathon.

The challenge required us to build an agent-based narrative system capable of maintaining state, producing varied actions, tracking entities, and resolving a generated mystery.

The project was built under hackathon time constraints and combined:

multi-agent orchestration

LLM-based decision making

state management

structured outputs

backend development

frontend visualization



---

Team

<div align="center">🌙 Midnight Sons

Moiz Ali Siddiqui
Syed Ayaan Nadeem
Talha Ahmad

Hackfest × Datathon 2026
IBA Karachi

</div>
---

License

This project is licensed under the MIT License.

See the LICENSE file for details.


---

Acknowledgments

LangGraph

Google Gemini

Next.js

IBA Karachi for hosting Hackfest × Datathon 2026



---

<div align="center">Built by Team Midnight Sons

For additional implementation details, see the technical documentation included in the repository.

</div>