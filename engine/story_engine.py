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
        self.last_danger_level = 'none'  # Track for consequence feedback
    
    def process_choice(self, choice_text: str, choice_index: int) -> Dict:
        """Process a player choice and modify stats."""
        self.choice_count += 1
        self.choice_history.append(choice_text)
        
        # Store last danger level for feedback
        self.last_danger_level = 'none'
        
        # Modify stats based on choice characteristics
        self._apply_choice_effects(choice_text, choice_index)
        
        # Update instability level
        self._update_instability()
        
        # Return current context for AI generation
        return self.get_context()
    
    def _apply_choice_effects(self, choice_text: str, choice_index: int):
        """Apply stat modifications based on choice content."""
        text_lower = choice_text.lower()
        
        # Check for dangerous choices FIRST (consequences)
        danger_level = self._assess_choice_danger(text_lower)
        self.last_danger_level = danger_level  # Store for feedback
        self._apply_consequences(danger_level, text_lower)
        
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
    
    def _assess_choice_danger(self, choice_text: str) -> str:
        """
        Assess danger level of a choice.
        Returns: 'none', 'low', 'medium', 'high', 'extreme'
        """
        # Keywords indicating danger levels
        extreme_keywords = ['attack', 'charge', 'confront directly', 'fight']
        high_keywords = ['investigate', 'touch', 'open', 'enter', 'confront']
        medium_keywords = ['explore', 'examine closely', 'follow', 'pursue']
        low_keywords = ['look', 'listen', 'observe', 'cautious']
        
        # Instant death trap check (1-2% for obvious traps)
        if any(word in choice_text for word in ['obvious trap', 'clearly dangerous', 'suicide']):
            if random.random() < 0.015:  # 1.5% chance
                return 'instant_death'
        
        # Check keywords
        if any(word in choice_text for word in extreme_keywords):
            return 'extreme'
        elif any(word in choice_text for word in high_keywords):
            return 'high'
        elif any(word in choice_text for word in medium_keywords):
            return 'medium'
        elif any(word in choice_text for word in low_keywords):
            return 'low'
        
        return 'none'
    
    def _apply_consequences(self, danger_level: str, choice_text: str):
        """Apply health and sanity consequences based on danger."""
        # Scale danger based on progression
        progression_multiplier = 1.0
        if self.choice_count > 20:
            progression_multiplier = 1.5  # Late game is more dangerous
        elif self.choice_count > 10:
            progression_multiplier = 1.2  # Mid game moderately dangerous
        
        # Apply consequences based on danger level
        if danger_level == 'instant_death':
            # Instant death trap triggered
            self.character_stats['health'] = 0
            self.trigger_event('instant_death_trap')
            return
        
        elif danger_level == 'extreme':
            # 20-30 health loss
            damage = random.randint(20, 30)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self._modify_hidden_stat('sanity', random.randint(-2, -1))
        
        elif danger_level == 'high':
            # 15-25 health loss
            damage = random.randint(15, 25)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self._modify_hidden_stat('sanity', random.randint(-1, 0))
        
        elif danger_level == 'medium':
            # 10-20 health loss
            damage = random.randint(10, 20)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
        
        elif danger_level == 'low':
            # 5-10 health loss
            damage = random.randint(5, 10)
            if self.choice_count > 10:
                damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
        
        # Random sanity drain (paranoia, witnessing horror)
        if 'horror' in choice_text or 'witness' in choice_text:
            self._modify_hidden_stat('sanity', random.randint(-2, -1))
        
        # Paranoid choices reduce sanity
        if 'paranoid' in choice_text or 'suspicious' in choice_text:
            self._modify_hidden_stat('sanity', -1)
    
    def get_consequence_feedback(self, danger_level: str) -> Optional[str]:
        """Get narrator feedback about consequences taken."""
        if danger_level == 'none':
            return None
        
        feedbacks = {
            'extreme': [
                "(that was unwise)",
                "(brave, but stupid)",
                "You pay the price.",
                "(ouch)",
            ],
            'high': [
                "(that cost you)",
                "Your health suffers.",
                "(was it worth it?)",
                "Pain follows."
            ],
            'medium': [
                "(careful...)",
                "That hurt.",
                "(consequences)",
            ],
            'low': [
                "(minor damage)",
                "You're bruised.",
            ]
        }
        
        if danger_level in feedbacks:
            return random.choice(feedbacks[danger_level])
        
        return None
    
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

