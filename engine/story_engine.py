"""Core story engine with dual stat systems and state management."""

import random
from typing import Dict, List, Optional
from copy import deepcopy
from config.settings import (
    DEFAULT_CHARACTER_STATS,
    DEFAULT_HIDDEN_STATS,
    PROGRESSION_CONFIG,
    CRITICAL_EVENTS
)


class StoryEngine:
    """Manages game state, stats, and progression."""
    
    def __init__(self):
        """Initialize the story engine."""
        self.character_stats = deepcopy(DEFAULT_CHARACTER_STATS)
        self.hidden_stats = deepcopy(DEFAULT_HIDDEN_STATS)
        self.choice_count = 0
        self.choice_history: List[str] = []
        self.event_flags: List[str] = []
        self.current_narrative = ""
        self.instability_level = 0
    
    def process_choice(self, choice_text: str, choice_index: int) -> Dict:
        """Process a player choice and modify stats."""
        self.choice_count += 1
        self.choice_history.append(choice_text)
        
        # Modify stats based on choice characteristics
        self._apply_choice_effects(choice_text, choice_index)
        
        # Update instability level
        self._update_instability()
        
        # Return current context for AI generation
        return self.get_context()
    
    def _apply_choice_effects(self, choice_text: str, choice_index: int):
        """Apply stat modifications based on choice content."""
        text_lower = choice_text.lower()
        
        # Courage modifications
        if any(word in text_lower for word in ['attack', 'fight', 'confront', 'face', 'charge']):
            self._modify_hidden_stat('courage', random.randint(1, 2))
            self._modify_character_stat('strength', random.randint(-1, 1))
        elif any(word in text_lower for word in ['flee', 'hide', 'retreat', 'avoid', 'run']):
            self._modify_hidden_stat('courage', random.randint(-2, -1))
            self._modify_character_stat('speed', random.randint(0, 1))
        
        # Sanity modifications
        if any(word in text_lower for word in ['look', 'examine', 'study', 'observe', 'stare']):
            self._modify_hidden_stat('sanity', random.randint(-1, 0))
            self._modify_hidden_stat('curiosity', random.randint(1, 2))
        
        # Curiosity modifications
        if any(word in text_lower for word in ['open', 'read', 'touch', 'take', 'investigate']):
            self._modify_hidden_stat('curiosity', random.randint(1, 2))
            self._modify_hidden_stat('trust', random.randint(-1, 0))
        
        # Trust modifications
        if any(word in text_lower for word in ['listen', 'follow', 'trust', 'believe', 'accept']):
            self._modify_hidden_stat('trust', random.randint(0, 2))
        elif any(word in text_lower for word in ['ignore', 'refuse', 'doubt', 'question', 'reject']):
            self._modify_hidden_stat('trust', random.randint(-2, 0))
            self._modify_hidden_stat('courage', random.randint(0, 1))
        
        # Random sanity drain (the world is unstable)
        if random.random() < 0.3:
            self._modify_hidden_stat('sanity', -1)
        
        # Health modifications (occasional danger)
        if random.random() < 0.15:
            self._modify_character_stat('health', random.randint(-15, -5))
    
    def _modify_hidden_stat(self, stat: str, change: int):
        """Modify a hidden stat (clamped 0-10)."""
        if stat in self.hidden_stats:
            self.hidden_stats[stat] = max(0, min(10, self.hidden_stats[stat] + change))
    
    def _modify_character_stat(self, stat: str, change: int):
        """Modify a character stat."""
        if stat in self.character_stats:
            if stat == 'health':
                # Health clamped to 0-max_health
                self.character_stats[stat] = max(
                    0, 
                    min(self.character_stats['max_health'], self.character_stats[stat] + change)
                )
            else:
                # Other stats clamped to 1-10
                self.character_stats[stat] = max(1, min(10, self.character_stats[stat] + change))
    
    def _update_instability(self):
        """Update instability level based on progression."""
        # Choice-based progression
        threshold = PROGRESSION_CONFIG['instability_choice_threshold']
        self.instability_level = self.choice_count // threshold
        
        # Stat-based modifiers
        if self.hidden_stats['sanity'] < 3:
            self.instability_level += 2
        if self.hidden_stats['trust'] < 2:
            self.instability_level += 1
        
        # Event-based spikes
        for event in self.event_flags:
            if event in CRITICAL_EVENTS:
                self.instability_level += 1
    
    def trigger_event(self, event_name: str):
        """Trigger a critical event that affects instability."""
        if event_name not in self.event_flags:
            self.event_flags.append(event_name)
            self._update_instability()
    
    def get_visual_intensity(self) -> str:
        """Get current visual effect intensity level."""
        if self.choice_count >= PROGRESSION_CONFIG['reality_collapse_at']:
            return 'collapsed'
        elif self.choice_count >= PROGRESSION_CONFIG['major_breakdown_at']:
            return 'breaking'
        elif self.choice_count >= PROGRESSION_CONFIG['minor_breakdown_at']:
            return 'disturbed'
        elif self.instability_level > 0:
            return 'unsettled'
        return 'stable'
    
    def get_context(self) -> Dict:
        """Get current context for AI generation."""
        return {
            'character_stats': self.character_stats.copy(),
            'hidden_stats': self.hidden_stats.copy(),
            'choice_count': self.choice_count,
            'previous_choice': self.choice_history[-1] if self.choice_history else 'BEGIN',
            'recent_narrative': self.current_narrative,
            'instability_level': self.instability_level,
            'visual_intensity': self.get_visual_intensity(),
            'event_flags': self.event_flags.copy()
        }
    
    def set_narrative(self, narrative: str):
        """Update current narrative text."""
        self.current_narrative = narrative
    
    def is_game_over(self) -> tuple[bool, Optional[str]]:
        """Check if game has ended."""
        # Death
        if self.character_stats['health'] <= 0:
            return True, "TERMINATION: Biological systems offline."
        
        # Sanity collapse
        if self.hidden_stats['sanity'] <= 0:
            return True, "TERMINATION: Coherence failure. You are no longer you."
        
        # Maximum choices reached (story exhaustion)
        if self.choice_count >= 30:
            return True, "TERMINATION: The story has run out of itself."
        
        return False, None
    
    def get_state_summary(self) -> Dict:
        """Get complete state for ghost memory saving."""
        return {
            'character_stats': self.character_stats,
            'hidden_stats': self.hidden_stats,
            'choice_count': self.choice_count,
            'choice_history': self.choice_history,
            'event_flags': self.event_flags,
            'instability_level': self.instability_level
        }

