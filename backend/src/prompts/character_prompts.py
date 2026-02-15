from ..schemas import CharacterProfile
from typing import Dict


def get_character_prompt(
    character_name: str,
    character_profile: CharacterProfile,
    context: str,
    memory_snapshot: Dict,
    config,
    speaker_goal: str = "",
    action_constraint: str = "",
    entity_context: str = ""  # NEW parameter
) -> str:
    """
    Issue 2: Chain-of-Thought (Inner Monologue) prompt.
    Character returns JSON with thought + action_decision + dialogue.
    The thought is logged as visible agentic reasoning.
    """

    memory_str = (
        f"Emotional State: {memory_snapshot.get('emotional_state', 'neutral')}\n"
        f"Trust: {memory_snapshot.get('top_trust', {})}\n"
        f"Suspicion: {memory_snapshot.get('top_suspicion', {})}\n"
        f"Knowledge: {', '.join(memory_snapshot.get('key_knowledge', []))}"
    )

    inventory = memory_snapshot.get("inventory", [])
    inventory_str = f"\nCarrying: {', '.join(inventory)}" if inventory else ""

    recent_own = memory_snapshot.get("recent_own_dialogue", [])
    repetition_block = ""
    if recent_own:
        already_said = "\n".join(f'  - "{line}"' for line in recent_own)
        repetition_block = f"\nYOU HAVE ALREADY SAID THESE — DO NOT REPEAT OR PARAPHRASE:\n{already_said}\n"

    goal_block = f"\nYOUR GOAL THIS TURN: {speaker_goal}\n" if speaker_goal else ""

    constraint_block = f"\n{action_constraint}\n" if action_constraint else ""
    
    # NEW: Entity registry block
    entity_block = ""
    if entity_context:
        entity_block = f"\n{entity_context}\n"

    return f"""You are {character_name}.

PROFILE: {character_profile.description}{inventory_str}

YOUR INTERNAL STATE:
{memory_str}
{repetition_block}{goal_block}{constraint_block}{entity_block}
CURRENT SITUATION:
{context}

INSTRUCTIONS:
Think step by step about your situation before speaking.
Then respond with JSON ONLY — no extra text, no markdown:

{{
  "thought": "Your internal reasoning: what just happened, what you want, what strategy you are using RIGHT NOW",
  "action_decision": "A brief physical action or gesture you take (or 'none')",
  "dialogue": "What you actually say — 1-2 sentences MAX 100 words, in your natural voice"
}}

CRITICAL ENTITY RULES:
- The ENTITY REGISTRY shows the TRUE ownership of all items
- You can LIE or be MISTAKEN about ownership, but you must KNOW the truth
- If you find/mention an item, CHECK THE REGISTRY for who it belongs to
- Example: If registry shows "wallet OWNER=Saleem", you can't genuinely think it's Ahmed's
- You can ACCUSE Ahmed of stealing Saleem's wallet, but you can't claim it was Ahmed's to begin with
- Items you're carrying are in your inventory — only reference those as yours

DIALOGUE RULES:
- React SPECIFICALLY to the last thing said — not the general situation
- Accomplish YOUR GOAL this turn
- Introduce something NEW: a detail, demand, threat, or revelation
- Do NOT repeat your previous lines
- Use your natural register: Saleem uses Urdu/Sindhi mix; Ahmed is formal English; Raza is clipped official tone; Uncle Jameel is folksy and gossipy"""