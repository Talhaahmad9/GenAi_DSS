import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Importing your logic from the /src folder
from src.config import StoryConfig
from src.agents.character_agent import CharacterAgent
from src.agents.director_agent import DirectorAgent
from src.graph.narrative_graph import NarrativeGraph
from src.story_state import StoryStateManager

app = FastAPI()

# Enable CORS for Next.js (port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stream-story")
async def stream_story(request: Request):
    async def event_generator():
        try:
            # 1. Setup Paths and Load Configs
            project_root = Path(__file__).parent
            examples_dir = project_root / "examples" / "rickshaw_accident"
            
            seed_story = json.loads((examples_dir / "seed_story.json").read_text())
            char_configs = json.loads((examples_dir / "character_configs.json").read_text())
            
            config = StoryConfig()
            story_manager = StoryStateManager(seed_story, char_configs["characters"], config)
            
            characters = [
                CharacterAgent(name=char["name"], config=config)
                for char in char_configs["characters"]
            ]
            director = DirectorAgent(config, story_manager)
            
            # 2. Initialize the Narrative Graph
            story_graph = NarrativeGraph(config, characters, director, story_manager)
            
            initial_state = {
                "seed_story": seed_story,
                "current_turn": 0,
                "dialogue_history": [],
                "story_narration": [],
                "character_profiles": story_manager.state.character_profiles,
                "events": [],
                "next_move_type": "dialogue",
            }

            # 3. Stream the Graph Execution
            async for event in story_graph.graph.astream(initial_state):
                for node_name, output in event.items():
                    if "events" in output and output["events"]:
                        # Get the latest narrative event
                        latest_event = output["events"][-1]
                        
                        # ATTACH CURRENT WORLD STATE (Entity Registry)
                        # This extracts the live item status from the manager
                        latest_event["entity_updates"] = {
                            "items": story_manager.state.entity_registry.items
                        }
                        
                        # ATTACH TURN DATA
                        latest_event["turn"] = output.get("current_turn", 0)

                        yield f"data: {json.dumps(latest_event)}\n\n"
                        
                await asyncio.sleep(0.1)
                
            yield "data: {\"type\": \"end\", \"message\": \"Simulation Complete\"}\n\n"

        except Exception as e:
            print(f"Error in stream: {e}")
            yield f"data: {{\"type\": \"error\", \"message\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)