import json
import random
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from .base_agent import BaseAgent
from ..config import StoryConfig
from ..schemas import StoryState
from ..prompts.director_prompts import DIRECTOR_SELECT_SPEAKER_PROMPT

# ─── Issue 1: Plot Clock ───────────────────────────────────────────────────────
# 3 strict phases. Director knows exactly where it is at all times.

PLOT_CLOCK = [
    {
        "name": "escalation",
        "turns": (1, 5),
        "goal": "Establish the accident scene. All characters introduced. Friction and accusations begin. NO resolution yet.",
        "pressure": "low",
        "speaker_mandates": {
            # Each character's job in this phase
            "Saleem":          "Establish innocence. Invoke family and livelihood. Deny fault.",
            "Ahmed Malik":     "Assert status. Invoke flight urgency. Demand accountability.",
            "Constable Raza":  "Establish authority. Size up the bribe opportunity. Stay ambiguous.",
            "Uncle Jameel":    "Insert himself. Pick a side (Saleem's). Offer unsolicited mediation."
        }
    },
    {
        "name": "complexity",
        "turns": (6, 12),
        "goal": "Sides harden. Bribe negotiation begins. Actions complicate the scene. Mystery clues start dropping.",
        "pressure": "high",
        "speaker_mandates": {
            "Saleem":          "React to specific accusations. Show desperation. Reveal new evidence or detail.",
            "Ahmed Malik":     "Escalate legal threats. React to Raza's bribe signal. Contradict himself under pressure.",
            "Constable Raza":  "Negotiate openly. Pressure the weaker party (Saleem). Reveal corrupt intent.",
            "Uncle Jameel":    "Drop clues. Threaten to expose Raza. Shift power dynamics."
        }
    },
    {
        "name": "resolution",
        "turns": (13, 99),
        "goal": "Force an outcome. Someone concedes, flees, or is exposed. The mystery truth drives the ending.",
        "pressure": "critical",
        "speaker_mandates": {
            "Saleem":          "Use the mystery clue if it favours you. Accept or reject the bribe outcome.",
            "Ahmed Malik":     "Face the consequences of your escalation. Concede, flee, or double down.",
            "Constable Raza":  "Bribe succeeds or collapses. React to any witnesses or superior officers.",
            "Uncle Jameel":    "Deploy the weapon clue. Force the decisive moment."
        }
    }
]

# ─── Hard Narrative Interventions ─────────────────────────────────────────────
# Fired at turn 15 if no resolution motion detected.

HARD_INTERVENTIONS = [
    {
        "id": "second_mobile",
        "narration": "A second police mobile pulls up, lights on. Constable Raza stiffens — his superior is inside.",
        "effect": "Raza must act clean or lose his job. The bribe window slams shut.",
        "knowledge": {"Constable Raza": "superior_officer_arrived_bribe_impossible"}
    },
    {
        "id": "airline_gate",
        "narration": "Ahmed's phone rings. The gate agent: 'Mr. Malik, boarding closes in twelve minutes.'",
        "effect": "Ahmed's leverage collapses. He needs to leave now, not win.",
        "knowledge": {"Ahmed Malik": "flight_closing_must_leave_immediately"}
    },
    {
        "id": "crowd_recording",
        "narration": "A teenager in the crowd raises his phone: 'Sab record ho raha hai — yeh live hai.' Three more phones go up.",
        "effect": "Bribe impossible on camera. Power shifts to Saleem.",
        "knowledge": {
            "Constable Raza": "crowd_recording_bribe_impossible",
            "Ahmed Malik": "cannot_threaten_on_camera"
        }
    }
]

# ─── Turning Point Events ──────────────────────────────────────────────────────

TURNING_POINT_EVENTS = [
    {
        "id": "airline_call",
        "narration": "Ahmed's phone rings — the airline gate agent: 'Mr. Malik, boarding closes in eighteen minutes.'",
        "effect": "Ahmed's leverage collapses. He needs to leave NOW, not win.",
        "character_impacts": {
            "Ahmed Malik": "flight_closing_call_received",
            "Constable Raza": "ahmed_now_desperate_to_leave"
        }
    },
    {
        "id": "crowd_recording",
        "narration": "Three phones rise from the crowd simultaneously. Someone shouts: 'Sab record ho raha hai!'",
        "effect": "Raza cannot take a bribe openly. Power shifts to Saleem.",
        "character_impacts": {
            "Constable Raza": "crowd_recording_bribe_impossible",
            "Ahmed Malik": "cannot_threaten_on_camera",
            "Saleem": "crowd_is_on_my_side"
        }
    },
    {
        "id": "dashcam_revealed",
        "narration": "Uncle Jameel holds up his phone — shaky footage of the exact moment of impact, shot from his shop doorway.",
        "effect": "Footage shows Ahmed's car drifting into Saleem's lane. Fault is now visible.",
        "character_impacts": {
            "Uncle Jameel": "i_have_proof_of_what_happened",
            "Ahmed Malik": "dashcam_shows_i_am_at_fault",
            "Saleem": "i_am_proven_innocent"
        }
    }
]


class DirectorAgent(BaseAgent):
    """
    All major decisions are Python/deterministic.
    LLM used only for: speaker selection narration + speaker goal.
    """

    ACTION_TEMPLATES = {
        "Saleem": [
            "pulls out crumpled license from pocket to prove identity",
            "frantically searches rickshaw for registration papers",
            "shows Ahmed the worn brake pedal explaining mechanical issues",
            "calls his wife on phone in panic about losing day's earnings",
            "points to tyre marks on road showing where impact happened",
            "opens rickshaw hood revealing engine damage from collision"
        ],
        "Ahmed Malik": [
            "aggressively inspects car damage while photographing with expensive phone",
            "pulls out business card threatening legal action",
            "checks watch repeatedly muttering about flight time",
            "demands to see Saleem's papers while recording on phone",
            "calls someone — possibly a lawyer or police contact",
            "points to paint scratch insisting on immediate compensation"
        ],
        "Constable Raza": [
            "pulls out citation book flipping through pages slowly",
            "walks around vehicles examining damage with flashlight",
            "signals other officers to redirect traffic",
            "suggests moving to side while hinting at facilitation fee",
            "lowers voice and speaks to Ahmed privately away from crowd",
            "ostentatiously writes in notebook while watching Saleem"
        ],
        "Uncle Jameel": [
            "steps between arguing parties waving hands dramatically",
            "points to scratch marks claiming he saw everything",
            "offers chai from his shop to calm everyone down",
            "pulls Raza aside whispering about proper procedure",
            "holds up phone showing he has been filming the scene",
            "addresses the crowd directly rallying them behind Saleem"
        ]
    }

    def __init__(self, config: StoryConfig, story_manager):
        super().__init__("Director", config)
        self.story_manager = story_manager
        self.turning_point_event = random.choice(TURNING_POINT_EVENTS)
        self.turning_point_fired = False
        self.intervention_fired = False
        self.last_speaker = None
        self.second_last_speaker = None
        
        # NEW: Track used actions to prevent repetition
        self.used_actions = set()

    # ── Issue 1: Plot Clock ────────────────────────────────────────────────────

    def get_current_phase(self) -> Dict:
        """Return current phase based on absolute turn number."""
        turn = self.story_manager.state.current_turn
        for phase in PLOT_CLOCK:
            lo, hi = phase["turns"]
            if lo <= turn <= hi:
                return phase
        return PLOT_CLOCK[-1]

    def get_speaker_mandate(self, character_name: str) -> str:
        phase = self.get_current_phase()
        return phase["speaker_mandates"].get(character_name, "React naturally to what just happened.")

    def _check_hard_intervention(self) -> Optional[Dict]:
        """
        Issue 1: Hard Narrative Intervention.
        Fires at turn 15 if we're still in complexity phase (no resolution motion).
        """
        turn = self.story_manager.state.current_turn
        phase = self.get_current_phase()

        if turn >= 15 and not self.intervention_fired and phase["name"] != "resolution":
            self.intervention_fired = True
            intervention = random.choice(HARD_INTERVENTIONS)
            # Apply knowledge to affected characters
            for char_name, knowledge_item in intervention.get("knowledge", {}).items():
                profile = self.story_manager.state.character_profiles.get(char_name)
                if profile:
                    profile.knowledge.add(knowledge_item)
            self._log_director_reasoning(
                "hard_intervention",
                f"Turn {turn}: No resolution at turn 15 — firing intervention: {intervention['id']}",
                intervention
            )
            return intervention
        return None

    def _fire_turning_point_if_needed(self) -> Optional[Dict]:
        phase = self.get_current_phase()
        if phase["name"] == "resolution" and not self.turning_point_fired:
            self.turning_point_fired = True
            for char_name, knowledge_item in self.turning_point_event["character_impacts"].items():
                profile = self.story_manager.state.character_profiles.get(char_name)
                if profile:
                    profile.knowledge.add(knowledge_item)
            return self.turning_point_event
        return None

    # ── Decision Logic ────────────────────────────────────────────────────────

    def _log_director_reasoning(self, decision_type: str, reason: str, metadata: Dict = None) -> None:
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": "Director",
            "decision_type": decision_type,
            "reason": reason,
            "turn": self.story_manager.state.current_turn,
            "metadata": metadata or {}
        })

    def decide_next_move(self) -> Tuple[str, Optional[str], Optional[Dict]]:
        current_turn = self.story_manager.state.current_turn

        if current_turn < 15 and self.story_manager.action_count < 5:
            if self.story_manager.should_force_action():
                return self._select_action()

        if self.story_manager.consecutive_dialogue_count >= 3:
            return self._select_action()

        if self.story_manager.should_escalate_tension():
            if random.random() > 0.5:
                return self._select_action()

        if current_turn > 5 and random.random() < 0.3:
            return self._select_action()

        return "dialogue", None, None

    def _select_action(self) -> Tuple[str, str, Dict]:
        available_chars = list(self.story_manager.state.character_profiles.keys())
        phase = self.get_current_phase()

        char_scores = []
        for char_name in available_chars:
            profile = self.story_manager.state.character_profiles[char_name]
            avg_suspicion = sum(profile.suspicion.values()) / max(len(profile.suspicion), 1)
            avg_trust = sum(profile.trust.values()) / max(len(profile.trust), 1)
            score = avg_suspicion - avg_trust + random.random() * 0.3
            char_scores.append((char_name, score))

        char_scores.sort(key=lambda x: x[1], reverse=True)
        selected_char = char_scores[0][0]

        all_actions = self.ACTION_TEMPLATES.get(selected_char, ["performs an action"])
        
        # NEW: Filter out already-used actions
        available_actions = [a for a in all_actions if a not in self.used_actions]
        
        # If all actions used, reset and allow reuse
        if not available_actions:
            self.used_actions.clear()
            available_actions = all_actions
        
        # Also filter by recent dialogue keywords (existing logic)
        used_lines = self.story_manager.character_dialogue_history.get(selected_char, [])
        recent_keywords = set()
        for line in used_lines[-3:]:
            recent_keywords.update(line.lower().split())
        preferred = [a for a in available_actions if not any(kw in a.lower() for kw in recent_keywords)]
        
        action_text = random.choice(preferred if preferred else available_actions)
        
        # NEW: Mark this action as used
        self.used_actions.add(action_text)

        other_chars = [c for c in available_chars if c != selected_char]
        targets = random.sample(other_chars, min(2, len(other_chars)))

        action_dict = {
            "character": selected_char,
            "action": action_text,
            "targets": targets,
            "effect": f"[{phase['name'].upper()}] {selected_char}: {action_text}"
        }

        self._log_director_reasoning(
            "action_selection",
            f"Phase={phase['name']} | turn={self.story_manager.state.current_turn} | "
            f"consecutive={self.story_manager.consecutive_dialogue_count} | actions={self.story_manager.action_count}",
            {"action": action_dict}
        )

        return "action", selected_char, action_dict

    # ── Speaker Selection ─────────────────────────────────────────────────────

    async def select_next_speaker(
        self, story_state: StoryState, available_characters: List[str]
    ) -> Tuple[str, Optional[str], Optional[str], Optional[Dict], Optional[Dict]]:
        """
        Returns: (next_speaker, narration, speaker_goal, turning_point_event, intervention_event)
        """
        intervention = self._check_hard_intervention()
        tp_event = self._fire_turning_point_if_needed()

        phase = self.get_current_phase()

        if story_state.dialogue_history:
            recent_dialogue = "\n".join(
                f"{t.speaker}: {t.dialogue}"
                for t in story_state.dialogue_history[-4:]
            )
        else:
            recent_dialogue = "No dialogue yet. The story is just starting."

        # Filter out speaker who spoke twice in a row
        filtered = available_characters[:]
        if self.last_speaker and self.second_last_speaker == self.last_speaker:
            if self.last_speaker in filtered and len(filtered) > 1:
                filtered = [c for c in filtered if c != self.last_speaker]

        # Active clue context
        clue_context = ""
        if story_state.current_turn in (5, 10, 15):
            clue = self.story_manager.get_clue_for_turn(story_state.current_turn)
            if clue:
                clue_context = f"\nACTIVE CLUE ({clue[0].upper()}): {clue[1]}"

        # Intervention/turning point override narration
        override_narration = ""
        if intervention:
            override_narration = intervention["narration"]
        elif tp_event:
            override_narration = tp_event["narration"]

        # NEW: Get entity context for Director
        entity_context = self.story_manager.get_entity_context()

        from ..prompts.director_prompts import DIRECTOR_SELECT_SPEAKER_PROMPT
        prompt = DIRECTOR_SELECT_SPEAKER_PROMPT.format(
            description=story_state.seed_story.get("description", ""),
            narrative_phase=phase["name"].upper(),
            phase_goal=phase["goal"],
            phase_turns=f"{phase['turns'][0]}–{phase['turns'][1]}",
            active_intervention=override_narration or "None",
            clue_context=clue_context,
            entity_context=entity_context,
            recent_dialogue=recent_dialogue,
            available_characters=", ".join(filtered)
        )

        response = await self.generate_response(prompt)

        try:
            cleaned = self._clean_json_response(response)
            data = json.loads(cleaned)
            next_speaker = data.get("next_speaker", filtered[0])
            narration = data.get("narration", "")
            speaker_goal = data.get("speaker_goal", "")

            if override_narration:
                narration = override_narration

            if next_speaker not in available_characters:
                next_speaker = filtered[0]

            # Inject phase mandate into speaker goal if LLM didn't set one
            if not speaker_goal:
                speaker_goal = self.get_speaker_mandate(next_speaker)

            self.second_last_speaker = self.last_speaker
            self.last_speaker = next_speaker

            self._log_director_reasoning(
                "speaker_selection",
                f"Phase={phase['name']} | Speaker={next_speaker} | Goal={speaker_goal}",
                {"speaker": next_speaker, "narration": narration, "goal": speaker_goal}
            )

            return next_speaker, narration, speaker_goal, tp_event, intervention

        except Exception as e:
            print(f"Director parse error: {e}")
            fallback = filtered[0]
            self.second_last_speaker = self.last_speaker
            self.last_speaker = fallback
            return fallback, override_narration or "", self.get_speaker_mandate(fallback), tp_event, intervention

    # ── Conclusion ────────────────────────────────────────────────────────────

    def check_conclusion_deterministic(self, story_state: StoryState) -> Tuple[bool, str, str]:
        current_turn = story_state.current_turn

        if current_turn < 15:
            return False, "Story must continue to minimum turn 15", ""

        if current_turn >= self.story_manager.total_turns:
            narration = self._generate_mystery_reveal()
            self._log_director_reasoning(
                "conclusion", f"Max turns reached ({self.story_manager.total_turns})",
                {"mystery": self.story_manager.hidden_truth}
            )
            return True, f"Story concluded at turn {current_turn}", narration

        if current_turn >= 18 and random.random() < 0.2:
            narration = self._generate_mystery_reveal()
            self._log_director_reasoning(
                "conclusion", f"Natural resolution at turn {current_turn}", {}
            )
            return True, f"Natural resolution at turn {current_turn}", narration

        return False, "", ""

    def _generate_mystery_reveal(self) -> str:
        """Generate a detailed 3-5 sentence conclusion that wraps up the story."""
        truth = self.story_manager.hidden_truth
        tp_id = self.turning_point_event["id"]

        # NEW: Detailed conclusions with 3-5 sentences
        reveals = {
            "saleem_innocent": (
                "Traffic camera footage later confirmed it: Ahmed's car had drifted lanes, clipping Saleem's rickshaw at the exact moment Ahmed glanced at his phone. "
                "Saleem stood vindicated, though the damage to his livelihood remained. "
                "Ahmed missed his flight, and the insurance claim would take months. "
                "Uncle Jameel returned to his chai stall, satisfied that justice—however messy—had been served. "
                "The crowd dispersed into the evening traffic, already forgetting the incident."
            ),
            "ahmed_stole_wallet": (
                "As Ahmed reached for his business card, Saleem's worn wallet tumbled from the briefcase onto the asphalt. "
                "The crowd went silent, then erupted. Constable Raza had no choice but to detain Ahmed for questioning. "
                "Saleem recovered his fifty thousand rupees, every note accounted for. "
                "Ahmed's flight departed without him, and his explanation to the airline—and later, his company—rang hollow. "
                "The footage of the wallet falling went viral by morning."
            ),
            "raza_corrupt": (
                "Uncle Jameel's nephew, already in the crowd with a press card, had been filming Constable Raza since the beginning. "
                "The footage aired that evening: Raza's whispered bribe negotiations, his hand extended toward Ahmed, the crowd's phones rising in unison. "
                "By morning, Raza was suspended pending investigation. "
                "Ahmed paid Saleem directly, settled the damages, and barely caught the last flight out. "
                "Shahrah-e-Faisal returned to its usual chaos, but Uncle Jameel's chai stall became a minor landmark—the place where a corrupt cop finally got caught."
            ),
            "wallet_never_stolen": (
                "Saleem's hand found the wallet wedged beneath the rickshaw seat—it had never left. "
                "Relief and embarrassment crossed his face simultaneously as he pulled out the familiar worn leather. "
                "Ahmed's impatience evaporated into exasperation; he'd missed his flight for nothing. "
                "Constable Raza pocketed his citation book, muttering about wasted time. "
                "The crowd dispersed, disappointed by the anticlimactic ending, as Karachi traffic swallowed them all."
            ),
            "uncle_witnessed_bribe": (
                "Uncle Jameel finally stepped forward: 'I saw Raza take money here three weeks ago from a truck driver. I have been waiting for a reason to say so.' "
                "The crowd turned on Constable Raza, who paled and began backing toward his motorcycle. "
                "Ahmed seized the opportunity, paid Saleem a quick settlement, and fled toward the airport. "
                "Raza's supervisor arrived within minutes—someone in the crowd had already called. "
                "Uncle Jameel returned to his stall, vindicated, as the evening call to prayer echoed across the city."
            )
        }

        tp_codas = {
            "airline_call":     " Ahmed had already missed his flight; the gate had closed three minutes before the wallet fell.",
            "crowd_recording":  " The footage was already uploading to three different social media platforms.",
            "dashcam_revealed": " The dashcam video was clear and undeniable, time-stamped and geotagged."
        }

        base = reveals.get(truth, (
            "The scene dissolved into the chaos of Karachi rush hour. "
            "Ahmed drove off toward the airport, unlikely to catch his flight. "
            "Saleem sat in his damaged rickshaw, calculating the cost of repairs. "
            "Constable Raza pocketed his citation book, unsatisfied. "
            "The crowd dispersed, and traffic swallowed them all."
        ))
        
        # Add turning point coda if it enhances the conclusion
        coda = tp_codas.get(tp_id, "")
        return base + coda

    async def check_conclusion(self, story_state: StoryState) -> Tuple[bool, Optional[str], Optional[str]]:
        return self.check_conclusion_deterministic(story_state)