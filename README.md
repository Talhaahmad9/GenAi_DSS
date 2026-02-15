<div align="center">

# 🎭 Multi-Agent Narrative Simulation Engine

### *Autonomous Agents. Dynamic Actions. Hidden Mysteries.*

[![Python](https://img.shields.io/badge/Python-3.11+-00ff41?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-00ff41?style=for-the-badge&logo=graphql&logoColor=black)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-Powered-00ff41?style=for-the-badge&logo=google&logoColor=black)](https://ai.google.dev)

**Team Midnight Sons** | Hackfest x IBA 2026

</div>

---

## 🚀 Quick Start Guide

### Prerequisites

```bash
Python 3.11+
UV package manager
Google Gemini API key
```

### Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/your-repo/GenAi_DSS.git
cd GenAi_DSS

# 2. Install dependencies
uv sync

# 3. Configure API key
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

# 4. Run simulation
uv run src/main.py
```

**⏱️ Execution time:** 3-5 minutes  
**📊 Output:** `story_output.json` + `prompts_log.json`

### Verification

```bash
# Check generated story
cat story_output.json | jq .

# Review agent reasoning
cat prompts_log.json | jq .
```

---

## 🐛 Troubleshooting

### API Key Error
```bash
# Ensure .env exists in root directory
echo "GOOGLE_API_KEY=your_actual_key" > .env
cat .env  # Verify
```

### Module Not Found
```bash
uv sync  # Reinstall dependencies
```

### Story Too Short/Long
Edit `src/story_state.py`:
```python
self.total_turns = random.randint(18, 22)  # Adjust range
```

---

## 📖 Overview

A production-grade **Multi-Agent Narrative System** where AI agents don't just talk—they **act, remember, and reason strategically**.

### ✨ What Makes This Different?

Traditional chatbots only generate dialogue. Our system creates **coherent, action-driven stories** where:

- 🎬 **Physical Actions** — Characters search, call, point, gesture (7+ per story)
- 🧠 **Chain-of-Thought** — Visible internal reasoning before every turn
- 💾 **Structured Memory** — Trust/suspicion scores evolve dynamically
- 📋 **Entity Tracking** — Prevents contradictions ("whose wallet is this?")
- 🔍 **Mystery System** — Hidden truth revealed through progressive clues

### 🎯 Sample Output

> *A 19-turn story about a rickshaw accident in Karachi where characters argue, perform actions (searching papers, making phone calls), and eventually reveal who stole the wallet.*

---

## 📁 Project Structure

```
GenAi_DSS/
├── 📂 examples/
│   └── rickshaw_accident/
│       ├── character_configs.json    # 4 character profiles
│       └── seed_story.json           # Story seed (mandatory)
│
├── 📂 src/
│   ├── 📂 agents/
│   │   ├── base_agent.py            # Abstract agent class
│   │   ├── character_agent.py       # CoT reasoning agent
│   │   └── director_agent.py        # Orchestrator agent
│   │
│   ├── 📂 graph/
│   │   └── narrative_graph.py       # LangGraph state machine
│   │
│   ├── 📂 prompts/
│   │   ├── character_prompts.py     # Character templates
│   │   └── director_prompts.py      # Director templates
│   │
│   ├── config.py                    # Configuration
│   ├── schemas.py                   # Pydantic models
│   ├── story_state.py               # State + entity registry
│   └── main.py                      # Entry point
│
├── 📄 story_output.json             # Generated narrative
├── 📄 prompts_log.json              # LLM interaction logs
└── 📄 README.md
```

---

## 🎯 System Architecture

### 1️⃣ The Director (Orchestrator)

```python
# Controls narrative flow through deterministic plot clock
PHASES = {
    "ESCALATION":  (1-5),    # Establish conflict
    "COMPLEXITY":  (6-12),   # Mystery clues, negotiations  
    "RESOLUTION":  (13+)     # Force conclusion
}
```

**Responsibilities:**
- ✅ Decides when characters speak vs. perform actions
- ✅ Selects next speaker using Gemini LLM
- ✅ Enforces minimum 5 actions before turn 15
- ✅ Injects turning points ("crowd starts recording")

---

### 2️⃣ Character Agents (TAD Loop)

```
┌─────────────────────────────────────┐
│  1. Receive Goal                    │
│     "Accuse Ahmed of stealing"      │
│           ↓                          │
│  2. Think (Chain-of-Thought)        │
│     "Ahmed is too calm..."          │
│           ↓                          │
│  3. Decide Action                   │
│     "none" or "points at briefcase" │
│           ↓                          │
│  4. Generate Dialogue                │
│     "Open that briefcase, Ahmed!"   │
└─────────────────────────────────────┘
```

**Output Example:**
```json
{
  "thought": "Ahmed is hiding something...",
  "action_decision": "none",
  "dialogue": "Open that briefcase, Ahmed sahib!"
}
```

---

### 3️⃣ State Manager

#### A. Entity Registry (Prevents Contradictions)

```json
{
  "wallet": {
    "owner": "Saleem",
    "status": "missing",
    "value": "50000 rupees"
  }
}
```

❌ **Without Registry:** *"I found a wallet... looks like Ahmed's!"*  
✅ **With Registry:** *"I found Saleem's wallet under the seat!"*

#### B. Character Memory (Evolves Over Time)

```json
{
  "trust": {"Ahmed": 0.3, "Saleem": 0.7},
  "suspicion": {"Raza": 0.8},
  "emotional_state": "angry",
  "knowledge": ["wallet_discussed", "bribe_attempted"]
}
```

---

### 4️⃣ Action System

**Enforcement Rules:**
```python
if turn < 15 and action_count < 5:
    if consecutive_dialogue >= 2:
        FORCE_ACTION = True

if consecutive_dialogue >= 3:
    FORCE_ACTION = True
```

**Action Handshaking:**
```
ACTION #3: Saleem frantically searches rickshaw
           ↓
Turn #4:   Ahmed MUST acknowledge this action
           "I observe Mr. Saleem's theatrical search..."
```

**Zero Repetition:**
- Global tracking prevents reuse
- 24+ unique templates per character
- Auto-reset only after full exhaustion

---

### 5️⃣ Mystery System

**Hidden Truth** (randomly selected):
- `saleem_innocent`
- `ahmed_stole_wallet`
- `wallet_never_stolen`
- `raza_corrupt`
- `uncle_witnessed_bribe`

**Progressive Clues:**
```
Turn 5:  Hint      → "Saleem pats pocket, goes pale"
Turn 10: Evidence  → "Ahmed shifts briefcase suspiciously"
Turn 15: Weapon    → "Uncle Jameel spots wallet corner"
Turn 19: Reveal    → "Wallet tumbles from briefcase..."
```

---

## 📊 Output Files

### 📄 story_output.json

Complete narrative trace with metadata:

```json
{
  "metadata": {
    "title": "The Rickshaw Accident",
    "dialogue_turns": 19,
    "actions_triggered": 7,
    "total_events": 26
  },
  "events": [
    {
      "type": "dialogue",
      "turn": 1,
      "speaker": "Ahmed Malik",
      "content": "This is preposterous...",
      "agentic_reasoning": {
        "thought": "I'm going to miss my flight...",
        "action_decision": "none"
      }
    },
    {
      "type": "action",
      "turn": 3,
      "character": "Saleem",
      "action": "points to tyre marks on road"
    },
    {
      "type": "conclusion",
      "turn": 19,
      "content": "As Ahmed reached for his card..."
    }
  ]
}
```

### 📄 prompts_log.json

Complete LLM interaction history:

```json
[
  {
    "timestamp": "2026-02-15T10:32:15.234Z",
    "agent": "Ahmed Malik",
    "agentic_reasoning": {
      "thought": "This Saleem is trying to distract...",
      "dialogue": "I observe Mr. Saleem's search..."
    }
  }
]
```

---

## 🔧 Configuration

### Change LLM Model

Edit `src/config.py`:

```python
class StoryConfig:
    model_name: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 1000
```

### Customize Characters

Edit `examples/rickshaw_accident/character_configs.json`:

```json
{
  "characters": [
    {
      "name": "Your Character",
      "description": "Personality and background..."
    }
  ]
}
```

### Add New Stories

1. Create folder in `examples/`
2. Add `seed_story.json` and `character_configs.json`
3. Update `src/main.py` to point to new story

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Entity-Ownership Registry

**Problem:** Characters claim wrong items  
**Solution:** Canonical registry  
**Result:** Zero contradictions

</td>
<td width="50%">

### 🧠 Chain-of-Thought

**Problem:** Can't see agent reasoning  
**Solution:** Visible `thought` field  
**Result:** Complete transparency

</td>
</tr>
<tr>
<td width="50%">

### 🔁 Zero-Repetition Actions

**Problem:** Same actions repeat  
**Solution:** Global tracking  
**Result:** 7+ unique actions

</td>
<td width="50%">

### ⏰ Deterministic Pacing

**Problem:** Stories meander  
**Solution:** Plot clock  
**Result:** Guaranteed resolution

</td>
</tr>
</table>

---

## 📚 Technical Stack

```yaml
Language:      Python 3.11+
LLM Provider:  Google Gemini 2.0 Flash
Framework:     LangGraph (LangChain)
State:         Pydantic v2
Package Mgr:   UV

API Calls:     ~45 per simulation
Cost:          ~$0.05 per run
Execution:     3-5 minutes
```

---

## 🎓 For Evaluators

### Quick Evaluation

```bash
# 1. Setup (one-time)
uv sync
echo "GOOGLE_API_KEY=your_key" > .env

# 2. Run
uv run src/main.py

# 3. Review outputs
cat story_output.json | jq .
cat prompts_log.json | jq .
```

### Key Files to Review

| File | What to Check |
|------|---------------|
| `story_output.json` | Generated narrative quality |
| `prompts_log.json` | Agent reasoning transparency |
| `src/agents/director_agent.py` | Action logic implementation |
| `src/story_state.py` | Entity registry implementation |
| `src/prompts/character_prompts.py` | Chain-of-Thought prompting |

### Evaluation Criteria

- ✅ **Actions:** 7+ unique, zero repetition
- ✅ **Entity Tracking:** Wallet ownership stays consistent
- ✅ **Chain-of-Thought:** Every turn has `thought` field
- ✅ **Conclusion:** 3-5 sentences revealing mystery

---

## 👥 Team

<div align="center">

**🌙 Midnight Sons 🌙**

Moiz Ali Siddiqui* • Syed Ayaan Nadeem • Talha Ahmad

*Institute of Business Administration (IBA), Karachi*

**Hackfest x Datathon 2026**

</div>

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- [LangGraph](https://langchain.com) for the agent framework
- [Google Gemini](https://ai.google.dev) for LLM capabilities
- IBA Karachi for hosting the competition

---

<div align="center">

**For detailed technical documentation, see the included PDF report.**

Made with 💚 by Midnight Sons

</div>
