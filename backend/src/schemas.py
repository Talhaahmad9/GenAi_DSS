from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from pydantic import BaseModel, Field

class DialogueTurn(BaseModel):
    turn_number: int
    speaker: str
    dialogue: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CharacterProfile(BaseModel):
    name: str
    description: str
    
    # Structured memory
    trust: Dict[str, float] = Field(default_factory=dict)
    suspicion: Dict[str, float] = Field(default_factory=dict)
    emotional_state: str = "neutral"
    knowledge: Set[str] = Field(default_factory=set)
    inventory: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True

# NEW: Entity Registry to track "who owns what"
class EntityRegistry(BaseModel):
    """Source of Truth for all items, claims, and ownership in the story."""
    items: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    # Structure: {"wallet": {"owner": "Saleem", "status": "missing", "value": "50000 rupees", "last_seen": "in rickshaw"}}
    
    def register_item(self, item_name: str, owner: str, **attributes):
        """Register an item with its owner and attributes."""
        self.items[item_name] = {
            "owner": owner,
            **attributes
        }
    
    def update_item_status(self, item_name: str, **updates):
        """Update item attributes (e.g., status, location)."""
        if item_name in self.items:
            self.items[item_name].update(updates)
    
    def get_item(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve item information."""
        return self.items.get(item_name)
    
    def get_owner(self, item_name: str) -> Optional[str]:
        """Get the owner of an item."""
        item = self.get_item(item_name)
        return item.get("owner") if item else None
    
    def get_items_by_owner(self, owner: str) -> List[str]:
        """Get all items owned by a character."""
        return [name for name, data in self.items.items() if data.get("owner") == owner]

class StoryState(BaseModel):
    seed_story: Dict[str, Any]
    current_turn: int = 0
    story_narration: List[str] = []
    dialogue_history: List[DialogueTurn] = Field(default_factory=list)
    events: List[Dict[str, Any]] = Field(default_factory=list)
    character_profiles: Dict[str, CharacterProfile] = Field(default_factory=dict)
    
    # Hidden truth
    hidden_truth: str = ""
    
    # NEW: Entity Registry
    entity_registry: EntityRegistry = Field(default_factory=EntityRegistry)
    
    # Director decision tracking
    next_move_type: str = "dialogue"
    next_action: Optional[Dict[str, Any]] = None
    
    # Controls
    next_speaker: Optional[str] = None
    director_notes: List[str] = []
    is_concluded: bool = False
    conclusion_reason: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True