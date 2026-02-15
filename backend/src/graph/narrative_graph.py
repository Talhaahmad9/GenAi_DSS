from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from ..config import StoryConfig
from ..schemas import StoryState, DialogueTurn
from ..agents.character_agent import CharacterAgent
from ..agents.director_agent import DirectorAgent
from ..story_state import StoryStateManager

class NarrativeGraph:
    def __init__(self, config: StoryConfig, characters: List[CharacterAgent],
                 director: DirectorAgent, story_manager: StoryStateManager):
        self.config = config
        self.characters = {c.name: c for c in characters}
        self.director = director
        self.story_manager = story_manager
        self.graph = self._build_graph()
        self.dialogue_turn_counter = 0
        self.action_counter = 0

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(StoryState)

        workflow.add_node("director_decide",    self._director_decide_node)
        workflow.add_node("execute_action",     self._execute_action_node)
        workflow.add_node("character_respond",  self._character_respond_node)
        workflow.add_node("check_conclusion",   self._check_conclusion_node)
        workflow.add_node("conclude",           self._conclude_node)

        workflow.set_entry_point("director_decide")

        workflow.add_conditional_edges(
            "director_decide",
            self._route_director_decision,
            {"action": "execute_action", "dialogue": "character_respond"}
        )

        workflow.add_edge("execute_action",    "check_conclusion")
        workflow.add_edge("character_respond", "check_conclusion")

        workflow.add_conditional_edges(
            "check_conclusion",
            self._route_conclusion,
            {"conclude": "conclude", "continue": "director_decide"}
        )

        workflow.add_edge("conclude", END)
        return workflow.compile()

    # ── Nodes ─────────────────────────────────────────────────────────────────

    async def _director_decide_node(self, state: StoryState) -> Dict:
        move_type, character, action_dict = self.director.decide_next_move()
        # Return only the new notes to be appended
        return {
            "director_notes": [f"Decision: {move_type}"],
            "next_move_type": move_type,
            "next_action": action_dict
        }

    async def _execute_action_node(self, state: StoryState) -> Dict:
        action_dict = state.next_action
        if not action_dict:
            return {}

        character  = action_dict["character"]
        action_text = action_dict["action"]
        targets    = action_dict.get("targets", [])

        # Update state via manager
        self.story_manager.update_memory_from_action(character, action_text, targets)
        self.story_manager.increment_action_count()
        self.story_manager.set_last_action(action_dict)

        self.action_counter += 1
        phase = self.director.get_current_phase()

        action_event = {
            "type": "action",
            "action_number": self.action_counter,
            "turn": state.current_turn,
            "character": character,
            "action": action_text,
            "effect": action_dict.get("effect", ""),
            "narrative_phase": phase["name"]
        }

        # FIX: Return only the NEW event array
        return {"events": [action_event]}

    async def _character_respond_node(self, state: StoryState) -> Dict:
        available = list(self.characters.keys())

        next_speaker, narration, speaker_goal, tp_event, intervention = \
            await self.director.select_next_speaker(state, available)

        character = self.characters[next_speaker]
        memory_snapshot  = self.story_manager.get_memory_snapshot(next_speaker)
        context          = self.story_manager.get_context_for_character(next_speaker)
        action_constraint = self.story_manager.get_action_constraint()
        entity_context = self.story_manager.get_entity_context()
        clue = self.story_manager.get_clue_for_turn(state.current_turn)

        dialogue, thought, action_decision = await character.respond(
            state, context, memory_snapshot, speaker_goal, action_constraint, entity_context
        )

        self.story_manager.update_memory_from_dialogue(next_speaker, dialogue, state.current_turn)
        self.story_manager.record_dialogue(next_speaker, dialogue)
        self.story_manager.increment_dialogue_count()
        self.dialogue_turn_counter += 1

        new_turn = DialogueTurn(
            turn_number=self.dialogue_turn_counter,
            speaker=next_speaker,
            dialogue=dialogue
        )

        events_update = []

        if intervention:
            events_update.append({
                "type": "hard_intervention",
                "turn": self.dialogue_turn_counter,
                "event_id": intervention["id"],
                "content": intervention["narration"],
                "effect": intervention["effect"]
            })

        if tp_event:
            events_update.append({
                "type": "turning_point",
                "turn": self.dialogue_turn_counter,
                "event_id": tp_event["id"],
                "content": tp_event["narration"],
                "effect": tp_event["effect"]
            })

        if clue:
            events_update.append({
                "type": "mystery_clue",
                "clue_type": clue[0],
                "turn": self.dialogue_turn_counter,
                "content": clue[1]
            })

        if narration:
            events_update.append({
                "type": "director_note",
                "turn": self.dialogue_turn_counter,
                "content": narration
            })

        events_update.append({
            "type": "dialogue",
            "turn": self.dialogue_turn_counter,
            "speaker": next_speaker,
            "content": dialogue,
            "agentic_reasoning": {
                "thought": thought,
                "action_decision": action_decision
            },
            "speaker_goal": speaker_goal
        })

        # FIX: Return only NEW turn and event list
        return {
            "dialogue_history": [new_turn],
            "current_turn":     state.current_turn + 1,
            "events":           events_update,
            "story_narration":  ([narration] if narration else [])
        }

    async def _check_conclusion_node(self, state: StoryState) -> Dict:
        should_end, reason, conclusion_narration = \
            self.director.check_conclusion_deterministic(state)

        events_update = []
        if should_end and conclusion_narration:
            events_update.append({
                "type": "conclusion",
                "turn": state.current_turn,
                "content": conclusion_narration
            })

        # FIX: Return only NEW conclusion event
        return {
            "is_concluded": should_end,
            "conclusion_reason": reason,
            "story_narration": ([conclusion_narration] if conclusion_narration else []),
            "events": events_update
        }

    async def _conclude_node(self, state: StoryState) -> Dict:
        return {"is_concluded": True}

    def _route_director_decision(self, state: StoryState) -> str:
        return state.next_move_type

    def _route_conclusion(self, state: StoryState) -> str:
        return "conclude" if state.is_concluded else "continue"

    async def run(self, seed_story: Dict, character_profiles: Dict[str, Any] = None) -> StoryState:
        initial_state = {
            "seed_story":          seed_story,
            "current_turn":        0,
            "dialogue_history":    [],
            "story_narration":     [],
            "character_profiles":  character_profiles or {},
            "director_notes":      [],
            "is_concluded":        False,
            "events":              [],
            "hidden_truth":        self.story_manager.hidden_truth,
            "next_move_type":      "dialogue",
            "next_action":         None,
            "entity_registry":     self.story_manager.state.entity_registry
        }
        return await self.graph.ainvoke(initial_state)