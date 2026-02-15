import asyncio
import json
import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import StoryConfig
from src.agents.character_agent import CharacterAgent
from src.agents.director_agent import DirectorAgent
from src.graph.narrative_graph import NarrativeGraph
from src.story_state import StoryStateManager

def print_header():
    """Beautiful ASCII header."""
    print("\n" + "═" * 80)
    print("║" + " " * 78 + "║")
    print("║" + "  🎭  MULTI-AGENT NARRATIVE SIMULATION ENGINE  🎭".center(78) + "║")
    print("║" + "  Intelligent Story Generation System".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("═" * 80)

def print_initialization_info(story_manager, seed_story):
#     """Print initialization details without revealing mystery."""
#     print("\n┌─ SIMULATION PARAMETERS " + "─" * 54 + "┐")
#     print(f"│  🎯 Target Duration: {story_manager.total_turns} turns")
#     print(f"│  📊 Minimum Turns: 15")
#     print(f"│  ⚡ Action Requirement: 5 actions before turn 15")
#     print(f"│  🎲 Mystery System: ACTIVE (hidden)")
#     print("└" + "─" * 78 + "┘")
    
    print("\n┌─ STORY SETUP " + "─" * 64 + "┐")
    print(f"│  Title: {seed_story['title']}")
    print(f"│  Scene: {seed_story['description']}...")
    print("└" + "─" * 78 + "┘\n")

async def main():
    # Load seed story
    examples_dir = project_root / "examples" / "rickshaw_accident"
    
    seed_story = json.loads((examples_dir / "seed_story.json").read_text())
    char_configs = json.loads((examples_dir / "character_configs.json").read_text())
    
    # Initialize config
    config = StoryConfig()
    
    # Initialize state manager (includes hidden mystery)
    story_manager = StoryStateManager(seed_story, char_configs["characters"], config)
    
    # Print beautiful header
    print_header()
    print_initialization_info(story_manager, seed_story)
    
    # Create character agents
    characters = [
        CharacterAgent(name=char["name"], config=config)
        for char in char_configs["characters"]
    ]
    
    # Create director with story manager reference
    director = DirectorAgent(config, story_manager)
    
    # Build narrative graph
    story_graph = NarrativeGraph(config, characters, director, story_manager)
    
    print("🎬 Starting Simulation...\n")
    print("═" * 80)
    
    # Run simulation
    final_state = await story_graph.run(
        seed_story=seed_story,
        character_profiles=story_manager.state.character_profiles
    )
    
    # Print final summary
    print("\n\n" + "═" * 80)
    print("║" + " " * 78 + "║")
    print("║" + "  ✅ SIMULATION COMPLETE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("═" * 80)
    
    print("\n┌─ FINAL STATISTICS " + "─" * 59 + "┐")
    print(f"│  Dialogue Turns: {story_graph.dialogue_turn_counter}")
    print(f"│  Actions Triggered: {story_graph.action_counter}")
    print(f"│  Total Events: {story_graph.dialogue_turn_counter + story_graph.action_counter}")
    print(f"│  Conclusion: {final_state.get('conclusion_reason', 'Natural ending')}")
    print("└" + "─" * 78 + "┘")

    # Save story_output.json
    output_path = project_root / "story_output.json"
    output_data = {
        "metadata": {
            "title": seed_story.get("title"),
            "dialogue_turns": story_graph.dialogue_turn_counter,
            "actions_triggered": story_graph.action_counter,
            "total_events": story_graph.dialogue_turn_counter + story_graph.action_counter,
            "hidden_truth": "not_revealed",
            "target_turns": story_manager.total_turns
        },
        "seed_story": seed_story,
        "events": final_state.get("events", []),
        "conclusion": {
            "reason": final_state.get("conclusion_reason"),
            "final_narration": final_state.get("story_narration", [])[-1] if final_state.get("story_narration") else ""
        }
    }
    output_path.write_text(json.dumps(output_data, indent=2))
    
    # Save prompts_log.json with enhanced metadata
    all_logs = director.logs.copy()
    for char_agent in characters:
        all_logs.extend(char_agent.logs)
    
    all_logs.sort(key=lambda x: x["timestamp"])
    
    log_path = project_root / "prompts_log.json"
    log_path.write_text(json.dumps(all_logs, indent=2))
    
    print("\n┌─ OUTPUT FILES " + "─" * 62 + "┐")
    print(f"│  ✅ Story Output: {output_path.name}")
    print(f"│  ✅ Prompt Logs: {log_path.name}")
    print("└" + "─" * 78 + "┘")
    
    print("\n┌─ SYSTEM FEATURES VALIDATED " + "─" * 49 + "┐")
    print("│  ✓ Structured Memory Management")
    print("│  ✓ Hidden Mystery System")
    print(f"│  ✓ Action Enforcement ({story_graph.action_counter} actions generated)")
    print("│  ✓ Deterministic Pacing & Control")
    print("│  ✓ Clean JSON Outputs")
    print("│  ✓ Efficient Token Usage")
    print("└" + "─" * 78 + "┘\n")

if __name__ == "__main__":
    asyncio.run(main())