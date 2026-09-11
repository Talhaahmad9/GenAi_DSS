<div align="center">🎭 Multi-Agent Narrative Simulation Engine

Autonomous Agents. Dynamic Actions. Persistent World State.

   

Team Midnight Sons
1st Place — IBA Hackfest × Datathon 2026

</div>
---

Overview

The Multi-Agent Narrative Simulation Engine is an agent-based storytelling system built for IBA Hackfest × Datathon 2026.

Instead of generating an entire story in a single LLM response, the system creates a persistent simulated world where autonomous agents make decisions, perform actions, interact with other characters, maintain memory, and gradually progress toward the resolution of a hidden mystery.

The simulation is coordinated through LangGraph, while structured state and agent outputs are maintained using Pydantic.

The project includes:

Autonomous character agents

A director/orchestrator agent

Persistent world and character state

Entity ownership tracking

Structured agent actions

Dynamic narrative progression

Simulation and decision logs

A Next.js dashboard for control and visualization



---

Key Features

Multi-Agent Orchestration

Multiple autonomous agents operate inside the same simulated world.

Each agent can:

Inspect the current world state

React to previous events

Use relevant character memory

Select an action

Interact with other characters

Affect tracked entities

Influence the direction of the story


A central director agent helps coordinate the simulation and narrative progression.

Persistent World State

The simulation maintains state across turns rather than treating every model request independently.

Tracked state includes:

Character information

Character memory

Previous actions

Narrative events

Entity ownership

Global story state

Simulation progress


Pydantic models are used to validate and structure this data.

Entity Ownership Registry

The engine includes a global entity registry to help maintain consistency across the simulation.

For example, if an important object belongs to a particular character, that ownership remains tracked across later turns rather than being recreated inconsistently by the model.

Structured Agent Decisions

Agent responses are processed as structured outputs rather than relying entirely on unvalidated free-form text.

Each turn can contain information such as:

Current interpretation of the situation

Selected action

Dialogue

Affected entities

Target characters

Resulting state changes


Dynamic Narrative Progression

The simulation progresses across multiple turns.

Characters gradually:

Discover information

React to previous events

Interact with one another

Change the world state

Move toward a final narrative resolution


The generated result is stored in:

story_output.json

Simulation and agent logs are stored in:

prompts_log.json

Interactive Frontend

The project includes a Next.js frontend for controlling and inspecting the simulation.

The interface supports:

Starting the simulation

Stopping the simulation

Stepping through turns

Viewing agent actions

Viewing the event feed

Inspecting world state

Inspecting character memory and state



---

Architecture

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


---

Project Structure

GenAi_DSS/
├── backend/
│   ├── examples/                  # Story seeds and character configurations
│   ├── src/
│   │   ├── agents/               # Character and director agent logic
│   │   ├── graph/                # LangGraph workflow
│   │   ├── prompts/              # Prompt templates
│   │   ├── config.py             # LLM and application configuration
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


---

Tech Stack

Area	Technology

Backend Language	Python 3.11+
Agent Framework	LangGraph / LangChain
LLM	Google Gemini 2.0 Flash
State Validation	Pydantic v2
Package Manager	UV
Frontend	Next.js / React
Styling	Tailwind CSS
Backend Communication	API
Output Format	JSON
Approx. API Calls	~45 per simulation
Typical Runtime	~3–5 minutes


> Runtime and API usage may vary depending on the simulation configuration and model behavior.




---

Quick Start

Prerequisites

Make sure you have the following installed:

Python 3.11+

UV

Node.js 18+

npm or Yarn

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

Run the Simulation from the CLI

uv run src/main.py

After execution, the simulation generates:

story_output.json
prompts_log.json

Start the Backend Server

The frontend requires the backend server to be running.

python server.py


---

Frontend Setup

Open another terminal and run:

cd frontend
npm install
npm run dev

Then open:

http://localhost:3000

Make sure the backend server is running before using the frontend.


---

Frontend Capabilities

The dashboard allows users to:

Start a simulation

Stop execution

Progress through the simulation step-by-step

View agent actions

Follow the event feed

Inspect world state

Inspect character memory

Monitor simulation progression



---

Simulation Flow

A simplified simulation cycle looks like this:

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

The process continues until the configured simulation length is reached and the narrative concludes.


---

Generated Outputs

Narrative Output

backend/story_output.json

Contains the generated narrative and resulting story events.

Simulation Logs

backend/prompts_log.json

Contains structured logs from the simulation, useful for:

Debugging

Evaluating agent behavior

Inspecting decisions

Understanding narrative progression



---

Key Files

File	Purpose

src/agents/	Character and director agent logic
src/graph/	LangGraph orchestration
src/prompts/	Agent prompt definitions
src/story_state.py	Global story state and entity registry
src/schemas.py	Pydantic schemas and structured outputs
src/config.py	Model and system configuration
server.py	Backend server
story_output.json	Final narrative output
prompts_log.json	Simulation and debugging logs



---

Evaluation Goals

The system was designed around several hackathon evaluation requirements.

Action Diversity

Agents should perform varied and meaningful actions instead of repeatedly choosing the same behavior.

Entity Consistency

Tracked objects should maintain consistent ownership and state throughout the simulation.

Structured Agent Output

Agent decisions are processed through structured schemas instead of relying entirely on unrestricted text generation.

Persistent State

Events from previous turns affect later decisions and narrative progression.

Narrative Resolution

The simulation gradually progresses toward a coherent conclusion that resolves the central mystery.


---

Troubleshooting

Missing Gemini API Key

Ensure the following file exists:

backend/.env

and contains:

GOOGLE_API_KEY=your_actual_key

Python Dependency Issues

Reinstall backend dependencies:

uv sync

Frontend Dependency Issues

rm -rf node_modules package-lock.json
npm install

If necessary:

npm cache clean --force

Port 3000 Already in Use

npx kill-port 3000

Then restart the frontend:

npm run dev

Adjust Simulation Length

The simulation length can be configured in the story state.

Example:

self.total_turns = random.randint(18, 22)


---

Hackathon

IBA Hackfest × Datathon 2026

Result: 1st Place

The project was developed by Team Midnight Sons during IBA Hackfest × Datathon 2026.

The challenge involved building an agent-based narrative system capable of:

Maintaining persistent state

Producing diverse actions

Tracking entities consistently

Coordinating multiple autonomous agents

Progressing toward a generated mystery resolution


The project combined:

Multi-agent orchestration

LLM-based decision making

Structured state management

Entity tracking

Backend development

Frontend visualization

Real-time simulation control



---

Team

<div align="center">🌙 Midnight Sons

Moiz Ali Siddiqui
Syed Ayaan Nadeem
Talha Ahmad

IBA Hackfest × Datathon 2026

</div>
---

Contributing

1. Fork the repository.


2. Create a feature branch.


3. Make your changes.


4. Test the backend or frontend as required.


5. Submit a pull request with a clear description of the changes.




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