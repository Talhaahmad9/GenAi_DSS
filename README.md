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
# Backend
Python 3.11+
UV package manager
Google Gemini API key

# Frontend
Node.js 18+
NPM or Yarn
```

### Installation & Setup

#### Backend
```bash
# 1. Clone repository
# (if not already done)
git clone https://github.com/your-repo/GenAi_DSS.git
cd GenAi_DSS/backend

# 2. Install dependencies
uv sync

# 3. Configure API key
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

# 4. Run simulation (for CLI output)
uv run src/main.py

# 5. (Required for frontend) Start backend server
python server.py
```

**⏱️ Execution time:** 3-5 minutes  
**📊 Output:** `story_output.json` + `prompts_log.json`

#### Frontend
```bash
cd ../frontend
npm install
# Make sure the backend server is running (python server.py in backend)!
npm run dev
# or
# yarn install && yarn dev
```

- Access the UI at [http://localhost:3000](http://localhost:3000)
- The frontend will visualize and control the simulation (see below for details)

### Verification

```bash
# Check generated story
cat story_output.json | jq .

# Review agent reasoning
cat prompts_log.json | jq .
```

---

## 📁 Project Structure

```
GenAi_DSS/
├── backend/
│   ├── examples/                  # Story seeds & character configs
│   ├── src/                      # Core simulation engine
│   │   ├── agents/               # Agent logic
│   │   ├── graph/                # Narrative state machine
│   │   ├── prompts/              # Prompt templates
│   │   ├── config.py             # LLM & system config
│   │   ├── schemas.py            # Pydantic models
│   │   ├── story_state.py        # State & registry
│   │   └── main.py               # Entry point
│   ├── story_output.json         # Generated narrative
│   ├── prompts_log.json          # LLM logs
│   └── ...
├── frontend/
│   ├── app/                      # Next.js app entry
│   ├── components/               # UI components
│   ├── public/                   # Static assets
│   ├── package.json              # Frontend dependencies
│   └── ...
└── README.md
```

---

## 🖥️ Frontend Usage

The frontend (Next.js/React) provides a live UI for simulation control and visualization.

**Note:** The backend server (`python server.py` in `backend/`) must be running before starting the frontend.

### Features
- Control simulation (start, stop, step)
- View event feed and agent actions
- Inspect world state and character memory

### Running the Frontend
```bash
cd frontend
npm install
# Make sure the backend server is running (python server.py in backend)!
npm run dev
```
Visit [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Environment Variables

- `GOOGLE_API_KEY` (backend): Your Gemini API key, set in `backend/.env`
- (Optional) Add other environment variables as needed for frontend/backend integration

---

## 🤝 Contributing

1. Fork the repo and create a feature branch
2. For backend: add/modify agents, prompts, or story logic in `backend/src/`
3. For frontend: add UI features in `frontend/components/`
4. Submit a pull request with clear description

---

## 🐛 Troubleshooting

### Backend

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

### Frontend
```bash
# If you see errors on npm install
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# If port 3000 is in use
npx kill-port 3000
```

---

## 📚 Technical Stack

```yaml
Backend Language: Python 3.11+
Backend LLM:     Google Gemini 2.0 Flash
Backend Framework: LangGraph (LangChain)
State:           Pydantic v2
Package Mgr:     UV
Frontend:        Next.js (React 18+)
UI:              Tailwind CSS
API Calls:       ~45 per simulation
Cost:            ~$0.05 per run
Execution:       3-5 minutes
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
