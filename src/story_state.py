from typing import List, Dict, Tuple, Optional, Set
from datetime import datetime
import random
from .schemas import StoryState, CharacterProfile, DialogueTurn, EntityRegistry
from .config import StoryConfig


MYSTERY_CLUES = {
    "saleem_innocent": {
        "hint":     "Uncle Jameel squints at the road surface — there are no skid marks from Saleem's side.",
        "evidence": "A bystander points out that Ahmed's car has pre-existing damage on the same panel.",
        "weapon":   "Uncle Jameel's phone shows a photo taken the moment after impact — Saleem's tyre tracks are perfectly straight."
    },
    "ahmed_stole_wallet": {
        "hint":     "Saleem suddenly pats his pocket and goes pale — his wallet is missing.",
        "evidence": "Ahmed shifts his briefcase to his other hand, blocking Saleem's line of sight to it.",
        "weapon":   "The wallet's corner is visible, protruding from Ahmed's briefcase flap."
    },
    "raza_corrupt": {
        "hint":     "Uncle Jameel watches Constable Raza carefully — he has seen this routine before.",
        "evidence": "Raza lowers his voice and moves Ahmed away from the crowd — the classic isolation move.",
        "weapon":   "Uncle Jameel speaks up: 'This constable tried the same thing on my street last month.'"
    },
    "wallet_never_stolen": {
        "hint":     "Saleem mentions his wallet in passing — then hesitates, unsure when he last had it.",
        "evidence": "Saleem searches his pockets frantically while arguing — it is not on his person.",
        "weapon":   "Uncle Jameel peers into the rickshaw and spots something wedged under the seat cushion."
    },
    "uncle_witnessed_bribe": {
        "hint":     "Uncle Jameel has been unusually quiet, watching Constable Raza with narrowed eyes.",
        "evidence": "Uncle Jameel pulls Saleem aside briefly and whispers something that makes Saleem stand straighter.",
        "weapon":   "Uncle Jameel steps forward: 'I have something to say about this constable that everyone here should hear.'"
    }
}


class StoryStateManager:
    MYSTERY_OPTIONS = [
        "saleem_innocent",
        "ahmed_stole_wallet",
        "raza_corrupt",
        "wallet_never_stolen",
        "uncle_witnessed_bribe"
    ]

    def __init__(self, seed_story: Dict, characters: List[Dict], config: StoryConfig):
        self.config = config
        self.hidden_truth = random.choice(self.MYSTERY_OPTIONS)

        character_profiles = {}
        character_names = [char["name"] for char in characters]

        for char in characters:
            name = char["name"]
            character_profiles[name] = CharacterProfile(
                name=name,
                description=char["description"],
                trust={other: 0.5 for other in character_names if other != name},
                suspicion={other: 0.3 for other in character_names if other != name},
                emotional_state="neutral",
                knowledge=set(),
                inventory=[]
            )

        self._initialize_mystery_knowledge(character_profiles)

        # NEW: Initialize Entity Registry
        entity_registry = EntityRegistry()
        self._initialize_entity_registry(entity_registry)

        self.state = StoryState(
            seed_story=seed_story,
            character_profiles=character_profiles,
            hidden_truth=self.hidden_truth,
            entity_registry=entity_registry  # NEW
        )

        self.total_turns = random.randint(18, 22)
        self.action_count = 0
        self.consecutive_dialogue_count = 0

        self.character_dialogue_history: Dict[str, List[str]] = {
            char["name"]: [] for char in characters
        }

        # Issue 4: Action context injection
        self.last_action_taken: Optional[Dict] = None
        self.last_action_acknowledged: bool = True

        # Issue 3: Volatility log
        self.memory_volatility_log: List[Dict] = []

        # Issue 5: Clue progression
        self.clues = MYSTERY_CLUES.get(self.hidden_truth, {})
        self.clues_dropped: Set[str] = set()

    def _initialize_mystery_knowledge(self, profiles: Dict) -> None:
        if self.hidden_truth == "saleem_innocent":
            profiles["Saleem"].knowledge.add("i_was_careful_driving")
            profiles["Uncle Jameel"].knowledge.add("saleem_is_good_driver")
        elif self.hidden_truth == "ahmed_stole_wallet":
            profiles["Ahmed Malik"].knowledge.add("i_have_saleems_wallet")
            profiles["Ahmed Malik"].inventory.append("saleem_wallet")
        elif self.hidden_truth == "raza_corrupt":
            profiles["Constable Raza"].knowledge.add("i_want_bribe_money")
        elif self.hidden_truth == "wallet_never_stolen":
            profiles["Saleem"].knowledge.add("my_wallet_is_in_rickshaw")
        elif self.hidden_truth == "uncle_witnessed_bribe":
            profiles["Uncle Jameel"].knowledge.add("i_saw_raza_take_bribe_before")

    # NEW: Initialize Entity Registry with canonical facts
    def _initialize_entity_registry(self, registry: EntityRegistry) -> None:
        """Register all key items at story start with their TRUE owners."""
        
        # Saleem's wallet (regardless of mystery)
        registry.register_item(
            "wallet",
            owner="Saleem",
            status="unknown",  # Will be updated as story progresses
            value="50000 rupees" if self.hidden_truth in ["wallet_never_stolen", "ahmed_stole_wallet"] else "unknown",
            last_seen="unknown"
        )
        
        # Ahmed's items
        registry.register_item(
            "flight_booking",
            owner="Ahmed Malik",
            status="valid",
            departure_time="urgent"
        )
        
        registry.register_item(
            "car",
            owner="Ahmed Malik",
            status="damaged",
            damage_location="front panel"
        )
        
        # Saleem's items
        registry.register_item(
            "rickshaw",
            owner="Saleem",
            status="damaged",
            registration="needs_checking"
        )
        
        # Update status based on mystery truth
        if self.hidden_truth == "wallet_never_stolen":
            registry.update_item_status("wallet", status="in_rickshaw", last_seen="under seat cushion")
        elif self.hidden_truth == "ahmed_stole_wallet":
            registry.update_item_status("wallet", status="stolen", last_seen="in Ahmed's briefcase")

    # NEW: Update entity registry when items are mentioned/discovered
    def update_entity_from_dialogue(self, speaker: str, dialogue: str) -> None:
        """Track item mentions and update registry."""
        dialogue_lower = dialogue.lower()
        registry = self.state.entity_registry
        
        # Track wallet mentions
        if "wallet" in dialogue_lower:
            if speaker == "Saleem":
                if "missing" in dialogue_lower or "lost" in dialogue_lower:
                    registry.update_item_status("wallet", status="missing", last_mentioned_by=speaker)
                elif "50000" in dialogue or "fifty thousand" in dialogue_lower:
                    registry.update_item_status("wallet", value="50000 rupees", claim_made_by=speaker)
            elif speaker == "Uncle Jameel":
                if "found" in dialogue_lower:
                    # Get the TRUE owner from registry
                    true_owner = registry.get_owner("wallet")
                    registry.update_item_status("wallet", status="found", found_by=speaker, location="rickshaw seat")

    # NEW: Get entity context for prompts
    def get_entity_context(self) -> str:
        """Return formatted entity registry for Director/Character prompts."""
        registry = self.state.entity_registry
        lines = ["ENTITY REGISTRY (Source of Truth):"]
        for item_name, data in registry.items.items():
            owner = data.get("owner", "unknown")
            status = data.get("status", "unknown")
            lines.append(f"  • {item_name}: OWNER={owner}, STATUS={status}")
        return "\n".join(lines)

    # ── Issue 5: Clue Progression ─────────────────────────────────────────────

    def get_clue_for_turn(self, current_turn: int) -> Optional[Tuple[str, str]]:
        """Returns (clue_type, clue_text) if a clue should drop this turn."""
        schedule = {5: "hint", 10: "evidence", 15: "weapon"}
        clue_type = schedule.get(current_turn)
        if clue_type and clue_type not in self.clues_dropped:
            clue_text = self.clues.get(clue_type)
            if clue_text:
                self.clues_dropped.add(clue_type)
                self._apply_clue_knowledge(clue_type)
                return clue_type, clue_text
        return None

    def _apply_clue_knowledge(self, clue_type: str) -> None:
        profiles = self.state.character_profiles
        truth = self.hidden_truth
        if clue_type == "hint":
            if truth == "wallet_never_stolen" and "Saleem" in profiles:
                profiles["Saleem"].knowledge.add("wallet_might_be_in_rickshaw")
            elif truth == "raza_corrupt" and "Uncle Jameel" in profiles:
                profiles["Uncle Jameel"].knowledge.add("raza_is_running_his_routine")
        elif clue_type == "evidence":
            if truth == "ahmed_stole_wallet" and "Ahmed Malik" in profiles:
                profiles["Ahmed Malik"].emotional_state = "nervous"
            elif truth == "raza_corrupt" and "Constable Raza" in profiles:
                profiles["Constable Raza"].emotional_state = "nervous"
        elif clue_type == "weapon":
            for profile in profiles.values():
                profile.knowledge.add(f"mystery_truth_emerging_{truth}")

    # ── Issue 4: Action Context Injection ────────────────────────────────────

    def set_last_action(self, action_dict: Dict) -> None:
        self.last_action_taken = action_dict
        self.last_action_acknowledged = False

    def get_action_constraint(self) -> str:
        if self.last_action_taken and not self.last_action_acknowledged:
            self.last_action_acknowledged = True
            char = self.last_action_taken.get("character", "someone")
            action = self.last_action_taken.get("action", "something")
            return (
                f"CONSTRAINT: You MUST directly react to {char} who just: {action}. "
                f"Acknowledge this explicitly — do not ignore it."
            )
        return ""

    # ── Issue 3: Perception Update (Volatile Memory) ──────────────────────────

    def update_memory_from_dialogue(self, speaker: str, dialogue: str, turn_number: int) -> None:
        dialogue_lower = dialogue.lower()
        profiles = self.state.character_profiles

        aggressive_signals = ["threaten", "sue", "lawyer", "arrest", "charge", "demand",
                              "incompetent", "preposterous", "idiot", "fool"]
        conciliatory_signals = ["please", "sorry", "understand", "calm", "settle",
                                "reasonable", "bhai", "yaar", "let us"]
        corruption_signals = ["chai pani", "facilitation", "settle quietly", "fee",
                              "between us", "nobody needs to know", "small amount"]
        victim_signals = ["family", "livelihood", "children", "cannot afford", "poor",
                          "mouths to feed"]

        is_aggressive    = any(s in dialogue_lower for s in aggressive_signals)
        is_conciliatory  = any(s in dialogue_lower for s in conciliatory_signals)
        is_corrupt       = any(s in dialogue_lower for s in corruption_signals)
        is_victim        = any(s in dialogue_lower for s in victim_signals)

        before_snapshot = self._snapshot_memory()

        for observer_name, observer_profile in profiles.items():
            if observer_name == speaker:
                continue

            if is_aggressive:
                observer_profile.suspicion[speaker] = min(
                    1.0, observer_profile.suspicion.get(speaker, 0.3) + 0.15)
                observer_profile.trust[speaker] = max(
                    0.0, observer_profile.trust.get(speaker, 0.5) - 0.10)

            if is_conciliatory:
                observer_profile.trust[speaker] = min(
                    1.0, observer_profile.trust.get(speaker, 0.5) + 0.08)

            if is_corrupt and speaker == "Constable Raza":
                observer_profile.suspicion[speaker] = min(
                    1.0, observer_profile.suspicion.get(speaker, 0.3) + 0.20)
                observer_profile.trust[speaker] = max(
                    0.0, observer_profile.trust.get(speaker, 0.5) - 0.15)

            if is_victim and speaker == "Saleem":
                observer_profile.trust[speaker] = min(
                    1.0, observer_profile.trust.get(speaker, 0.5) + 0.05)

        after_snapshot = self._snapshot_memory()
        self.memory_volatility_log.append({
            "turn": turn_number,
            "speaker": speaker,
            "before": before_snapshot,
            "after": after_snapshot,
            "signals": {
                "aggressive": is_aggressive,
                "conciliatory": is_conciliatory,
                "corrupt": is_corrupt,
                "victim": is_victim
            }
        })
        
        # NEW: Update entity registry from dialogue
        self.update_entity_from_dialogue(speaker, dialogue)

    def _snapshot_memory(self) -> Dict:
        return {
            name: {
                "trust": {k: round(v, 3) for k, v in p.trust.items()},
                "suspicion": {k: round(v, 3) for k, v in p.suspicion.items()},
                "emotional_state": p.emotional_state
            }
            for name, p in self.state.character_profiles.items()
        }

    # ── Existing: Memory Update from Actions ──────────────────────────────────

    def update_memory_from_action(self, character: str, action: str, targets: List[str] = None) -> None:
        profile = self.state.character_profiles.get(character)
        if not profile:
            return
        action_lower = action.lower()
        if "accuse" in action_lower or "blame" in action_lower:
            profile.emotional_state = "angry"
            if targets:
                for t in targets:
                    profile.suspicion[t] = min(1.0, profile.suspicion.get(t, 0.5) + 0.3)
                    profile.trust[t] = max(0.0, profile.trust.get(t, 0.5) - 0.2)
        elif "show" in action_lower or "reveal" in action_lower:
            profile.emotional_state = "defensive"
            if "wallet" in action_lower: profile.knowledge.add("wallet_discussed")
            if "damage" in action_lower: profile.knowledge.add("damage_shown")
        elif "demand" in action_lower or "threaten" in action_lower:
            profile.emotional_state = "aggressive"
            if targets:
                for t in targets:
                    profile.trust[t] = max(0.0, profile.trust.get(t, 0.5) - 0.3)
        elif "calm" in action_lower or "mediate" in action_lower:
            profile.emotional_state = "diplomatic"
            if targets:
                for t in targets:
                    profile.trust[t] = min(1.0, profile.trust.get(t, 0.5) + 0.1)
        elif "bribe" in action_lower or "fee" in action_lower or "money" in action_lower:
            profile.emotional_state = "nervous"
            profile.knowledge.add("bribe_attempted")
            if targets:
                for t in targets:
                    profile.suspicion[t] = min(1.0, profile.suspicion.get(t, 0.5) + 0.2)
        elif "search" in action_lower or "check" in action_lower:
            profile.emotional_state = "suspicious"
            if "rickshaw" in action_lower: profile.knowledge.add("rickshaw_searched")
        elif "leave" in action_lower or "walk" in action_lower:
            profile.emotional_state = "frustrated"
        profile.knowledge.add(f"action_{action_lower.replace(' ', '_')[:30]}")

    # ── Memory Snapshot for Prompts ───────────────────────────────────────────

    def get_memory_snapshot(self, character_name: str) -> Dict:
        profile = self.state.character_profiles.get(character_name)
        if not profile:
            return {}
        top_trust = sorted(profile.trust.items(), key=lambda x: x[1], reverse=True)[:2]
        top_suspicion = sorted(profile.suspicion.items(), key=lambda x: x[1], reverse=True)[:2]
        own_recent = self.character_dialogue_history.get(character_name, [])[-3:]
        return {
            "emotional_state": profile.emotional_state,
            "top_trust": {n: round(v, 2) for n, v in top_trust},
            "top_suspicion": {n: round(v, 2) for n, v in top_suspicion},
            "key_knowledge": list(profile.knowledge)[-4:],
            "inventory": profile.inventory,
            "recent_own_dialogue": own_recent
        }

    def get_context_for_character(self, character_name: str) -> str:
        recent = self.state.dialogue_history[-4:]
        history_text = "\n".join(
            f"{t.speaker}: {t.dialogue}" for t in recent
        ) if recent else "Story just started."
        
        # NEW: Add entity context
        entity_context = self.get_entity_context()
        
        return (
            f"Initial Event: {self.state.seed_story.get('description', 'Unknown event')}\n\n"
            f"{entity_context}\n\n"
            f"Recent Conversation:\n{history_text}"
        )

    def get_context_for_director(self) -> str:
        history_text = "\n".join(
            f"[{t.turn_number}] {t.speaker}: {t.dialogue}"
            for t in self.state.dialogue_history[-10:]
        )
        
        # NEW: Add entity context
        entity_context = self.get_entity_context()
        
        return (
            f"Story: {self.state.seed_story.get('title', 'Untitled')}\n"
            f"Event: {self.state.seed_story.get('description', '')}\n"
            f"{entity_context}\n"
            f"Recent Dialogue:\n{history_text}\n"
            f"Turn: {self.state.current_turn} / {self.total_turns}\n"
            f"Actions: {self.action_count}"
        )

    def add_turn(self, speaker: str, dialogue: str, metadata: Dict = None) -> None:
        turn = DialogueTurn(
            turn_number=self.state.current_turn + 1,
            speaker=speaker,
            dialogue=dialogue,
            metadata=metadata or {}
        )
        self.state.dialogue_history.append(turn)
        self.state.current_turn += 1

    def should_force_action(self) -> bool:
        if self.state.current_turn < 15 and self.action_count < 5:
            if self.consecutive_dialogue_count >= 2:
                return True
        if self.consecutive_dialogue_count >= 3:
            return True
        return False

    def should_escalate_tension(self) -> bool:
        return self.state.current_turn > 0 and self.state.current_turn % 4 == 0

    def increment_action_count(self) -> None:
        self.action_count += 1
        self.consecutive_dialogue_count = 0

    def increment_dialogue_count(self) -> None:
        self.consecutive_dialogue_count += 1

    def record_dialogue(self, speaker: str, dialogue: str) -> None:
        if speaker in self.character_dialogue_history:
            self.character_dialogue_history[speaker].append(dialogue)