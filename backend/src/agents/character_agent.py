from typing import List, Dict, Tuple
from datetime import datetime
import json
from .base_agent import BaseAgent
from ..config import StoryConfig
from ..schemas import StoryState
from ..prompts.character_prompts import get_character_prompt


class CharacterAgent(BaseAgent):
    """
    Character generates dialogue via Chain-of-Thought JSON.
    The 'thought' field is logged as visible agentic reasoning.
    Only 'dialogue' is shown in the CLI story output.
    """

    def __init__(self, name: str, config: StoryConfig):
        super().__init__(name, config)

    async def respond(
        self,
        story_state: StoryState,
        context: str,
        memory_snapshot: Dict,
        speaker_goal: str = "",
        action_constraint: str = "",
        entity_context: str = ""  # NEW parameter
    ) -> Tuple[str, str, str]:
        """
        Returns: (dialogue, thought, action_decision)
        dialogue       → shown in CLI
        thought        → logged as agentic reasoning (Issue 2)
        action_decision → logged and shown in CLI as minor gesture
        """
        character_profile = story_state.character_profiles.get(self.name)

        prompt = get_character_prompt(
            character_name=self.name,
            character_profile=character_profile,
            context=context,
            memory_snapshot=memory_snapshot,
            config=self.config,
            speaker_goal=speaker_goal,
            action_constraint=action_constraint,
            entity_context=entity_context  # NEW: Pass entity context
        )

        try:
            raw = await self.generate_response(prompt)
            dialogue, thought, action_decision = self._parse_cot_response(raw)
        except Exception as e:
            print(f"Error generating response for {self.name}: {e}")
            dialogue, thought, action_decision = "...", "", "none"

        self._log_cot_interaction(prompt, memory_snapshot, speaker_goal, thought, action_decision, dialogue)

        return dialogue, thought, action_decision

    def _parse_cot_response(self, raw: str) -> Tuple[str, str, str]:
        """Parse JSON CoT response. Graceful fallback if malformed."""
        try:
            cleaned = self._clean_json_response(raw)
            data = json.loads(cleaned)
            dialogue = data.get("dialogue", "").strip()
            thought = data.get("thought", "").strip()
            action_decision = data.get("action_decision", "none").strip()

            # Fallback: if dialogue is empty, use the raw response
            if not dialogue:
                dialogue = raw.strip()

            return dialogue, thought, action_decision
        except (json.JSONDecodeError, AttributeError):
            # If JSON parsing fails entirely, treat raw as plain dialogue
            return raw.strip(), "", "none"

    def _log_cot_interaction(
        self,
        prompt: str,
        memory_snapshot: Dict,
        speaker_goal: str,
        thought: str,
        action_decision: str,
        dialogue: str
    ) -> None:
        estimated_tokens = len(prompt) // 4
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "memory_snapshot": memory_snapshot,
            "speaker_goal": speaker_goal,
            "agentic_reasoning": {           # Issue 2: visible reasoning for judges
                "thought": thought,
                "action_decision": action_decision,
                "dialogue": dialogue
            },
            "estimated_tokens": estimated_tokens
        }
        self.logs.append(entry)