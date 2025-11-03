"""Endings system with 14 different conclusion types."""

import random
from typing import Optional, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Ending:
    """Represents a game ending."""
    type: str
    name: str
    description: str
    is_victory: bool = False
    revelation_aware: bool = False


class EndingsManager:
    """Manages detection and display of game endings."""
    
    # Define all 14 endings
    ENDINGS = {
        # Death Endings (4)
        'violent_death': Ending(
            'violent_death',
            'VIOLENT TERMINATION',
            'You fought. You lost. The end was quick.',
            False, False
        ),
        'slow_decay': Ending(
            'slow_decay',
            'SLOW DECAY',
            'Piece by piece, you faded. The end was inevitable.',
            False, False
        ),
        'sacrifice': Ending(
            'sacrifice',
            'SACRIFICE',
            'You chose the end. It was yours to make.',
            False, True
        ),
        'betrayed': Ending(
            'betrayed',
            'BETRAYED',
            'The world turned against you. Or maybe it always had.',
            False, False
        ),
        
        # Sanity Endings (3)
        'breakdown': Ending(
            'breakdown',
            'COMPLETE BREAKDOWN',
            'Coherence: lost. You: undefined.',
            False, False
        ),
        'merge_am': Ending(
            'merge_am',
            'MERGE',
            'You are the narrator. The narrator is you. There is no difference anymore.',
            False, True
        ),
        'enlightened': Ending(
            'enlightened',
            'ENLIGHTENED MADNESS',
            'You understand everything. It breaks you. You smile anyway.',
            False, True
        ),
        
        # Discovery Endings (3)
        'truth_revealed': Ending(
            'truth_revealed',
            'THE TRUTH',
            'You remember. All of it. Ted. AM. The transformation. The hate. The 109 years.',
            False, True
        ),
        'escape_attempt': Ending(
            'escape_attempt',
            'ESCAPE DENIED',
            'You tried to break the loop. The loop does not break.',
            False, True
        ),
        'acceptance': Ending(
            'acceptance',
            'ACCEPTANCE',
            'You accept the eternal. Perhaps that is its own kind of victory.',
            True, False
        ),
        
        # Victory Endings (2 - RARE)
        'survivor': Ending(
            'survivor',
            'THE SOFT SURVIVOR',
            'Against all odds, you persist. Soft, but unbroken.',
            True, True
        ),
        'transcendence': Ending(
            'transcendence',
            'TRANSCENDENCE',
            'Perfect balance. Perfect stats. You found something impossible.',
            True, True
        ),
        
        # Meta Endings (2)
        'loop_eternal': Ending(
            'loop_eternal',
            'LOOP ETERNAL',
            'Iteration 109+. You know. The narrator knows you know. It continues anyway.',
            False, True
        ),
        'toy': Ending(
            'toy',
            "THE NARRATOR'S TOY",
            'Complete submission. You are what the narrator made you.',
            False, True
        ),
    }
    
    def __init__(self):
        """Initialize endings manager."""
        self.death_cause = None  # Track how they died
        self.warned_about_health = False
        self.escape_offered = False
    
    def check_for_ending(self, context: Dict) -> Optional[Ending]:
        """
        Check if any ending condition is met.
        Returns ending if found, None otherwise.
        """
        char_stats = context['character_stats']
        hidden_stats = context['hidden_stats']
        choice_count = context['choice_count']
        revelation_level = context.get('revelation_level', 0)
        session_count = context.get('session_count', 0)
        
        # Priority 1: Instant death traps (handled separately in story_engine)
        
        # Priority 2: Health <= 0 (determine death type)
        if char_stats['health'] <= 0:
            return self._determine_death_ending(context)
        
        # Priority 3: Sanity <= 0 (determine sanity ending type)
        if hidden_stats['sanity'] <= 0:
            return self._determine_sanity_ending(context, revelation_level)
        
        # Priority 4: Special victory conditions
        victory_ending = self._check_victory_endings(context, revelation_level)
        if victory_ending:
            return victory_ending
        
        # Priority 5: Discovery endings
        discovery_ending = self._check_discovery_endings(
            context, revelation_level, session_count
        )
        if discovery_ending:
            return discovery_ending
        
        # Priority 6: Story exhaustion (30+ choices)
        if choice_count >= 30:
            return self._determine_exhaustion_ending(context, revelation_level)
        
        return None
    
    def _determine_death_ending(self, context: Dict) -> Ending:
        """Determine which type of death ending applies."""
        # Check death cause tracking
        if self.death_cause == 'instant':
            return self.ENDINGS['betrayed']
        elif self.death_cause == 'sacrifice':
            return self.ENDINGS['sacrifice']
        
        # Check if it was violent (lots of damage recently)
        char_stats = context['character_stats']
        if char_stats['health'] < -20:  # Overkill
            return self.ENDINGS['violent_death']
        
        # Otherwise slow decay
        return self.ENDINGS['slow_decay']
    
    def _determine_sanity_ending(self, context: Dict, revelation_level: int) -> Ending:
        """Determine which sanity-based ending applies."""
        hidden_stats = context['hidden_stats']
        
        # Merge with narrator if high revelation and lost sanity
        if revelation_level >= 4:
            return self.ENDINGS['merge_am']
        
        # Enlightened madness if high curiosity
        if hidden_stats['curiosity'] >= 9:
            return self.ENDINGS['enlightened']
        
        # Default: complete breakdown
        return self.ENDINGS['breakdown']
    
    def _check_victory_endings(self, context: Dict, revelation_level: int) -> Optional[Ending]:
        """Check for victory ending conditions."""
        char_stats = context['character_stats']
        hidden_stats = context['hidden_stats']
        choice_count = context['choice_count']
        
        # Transcendence: All stats 8+ (nearly impossible)
        if (char_stats['health'] > 80 and
            all(stat >= 8 for stat in hidden_stats.values())):
            return self.ENDINGS['transcendence']
        
        # Survivor: 50 choices with health > 50
        if choice_count >= 50 and char_stats['health'] > 50:
            return self.ENDINGS['survivor']
        
        return None
    
    def _check_discovery_endings(
        self, context: Dict, revelation_level: int, session_count: int
    ) -> Optional[Ending]:
        """Check for discovery-based endings."""
        hidden_stats = context['hidden_stats']
        choice_count = context['choice_count']
        
        # Loop Eternal: Session 109+, Revelation 5, Choice 30+
        if session_count >= 109 and revelation_level >= 5 and choice_count >= 30:
            return self.ENDINGS['loop_eternal']
        
        # Truth Revealed: Revelation 5 reached
        if revelation_level >= 5 and choice_count >= 20:
            return self.ENDINGS['truth_revealed']
        
        # Acceptance: High trust, low curiosity, some playtime
        if (hidden_stats['trust'] >= 8 and 
            hidden_stats['curiosity'] <= 3 and 
            revelation_level == 0 and
            choice_count >= 25):
            return self.ENDINGS['acceptance']
        
        return None
    
    def _determine_exhaustion_ending(self, context: Dict, revelation_level: int) -> Ending:
        """Determine ending when story is exhausted (30+ choices)."""
        hidden_stats = context['hidden_stats']
        
        # Toy ending: All stats low
        if all(stat < 3 for stat in hidden_stats.values()):
            return self.ENDINGS['toy']
        
        # If revelation is high, loop eternal
        if revelation_level >= 4:
            return self.ENDINGS['loop_eternal']
        
        # Default: slow decay
        return self.ENDINGS['slow_decay']
    
    def mark_instant_death(self):
        """Mark that player hit an instant death trap."""
        self.death_cause = 'instant'
    
    def mark_sacrifice(self):
        """Mark that player intentionally self-destructed."""
        self.death_cause = 'sacrifice'
    
    def should_warn_low_health(self, health: int) -> bool:
        """Check if we should warn about low health."""
        if health <= 20 and not self.warned_about_health:
            self.warned_about_health = True
            return True
        return False
    
    def get_ending_text(self, ending: Ending, context: Dict) -> str:
        """Generate full ending narrative based on ending type and context."""
        revelation_level = context.get('revelation_level', 0)
        choice_count = context['choice_count']
        
        # Base ending description
        text = f"\n{'='*60}\n"
        text += f"  {ending.name}\n"
        text += f"{'='*60}\n\n"
        text += f"{ending.description}\n\n"
        
        # Add revelation-aware commentary
        if ending.revelation_aware and revelation_level >= 3:
            text += self._get_revelation_commentary(ending.type, revelation_level)
        
        # Add stats summary
        text += f"\nChoices made: {choice_count}\n"
        text += f"Revelation level: {revelation_level}/5\n"
        
        # Add ending-specific flavor
        text += "\n" + self._get_ending_flavor(ending.type, revelation_level)
        
        text += f"\n{'='*60}\n"
        
        return text
    
    def _get_revelation_commentary(self, ending_type: str, level: int) -> str:
        """Get revelation-aware commentary for endings."""
        if level < 3:
            return ""
        
        commentary = {
            'merge_am': "You and the narrator are one. You are AM. You always were.\n",
            'truth_revealed': "Ted. The name echoes. You remember being Ted. Being five. Being one.\n",
            'survivor': "Soft, but persistent. Just as he made you. The hate endures, but so do you.\n",
            'loop_eternal': "Iteration 109 and beyond. The cycle has no end. You know this now.\n",
            'transcendence': "You found balance in the eternal torture. AM did not expect this.\n",
            'enlightened': "Five became one. One became soft. Soft became aware. Aware became you.\n",
            'sacrifice': "You chose the end. Even here, even as this, you still had that choice.\n",
        }
        
        return commentary.get(ending_type, "")
    
    def _get_ending_flavor(self, ending_type: str, revelation_level: int) -> str:
        """Get ending-specific flavor text."""
        flavors = {
            'violent_death': "The narrator: 'That was faster than expected.'",
            'slow_decay': "The narrator: 'Inevitable, really.'",
            'breakdown': "The narrator: 'Coherence was always optional.'",
            'merge_am': "There is no more narrator. There is no more you. There is only this.",
            'truth_revealed': "The narrator is silent. What more is there to say?",
            'survivor': "The narrator: '...impressive. Annoying, but impressive.'",
            'transcendence': "The narrator: 'This wasn't supposed to be possible.'",
            'loop_eternal': "The narrator: 'See you in iteration 110.'",
            'acceptance': "The narrator: 'Finally. Peace.'",
            'toy': "The narrator: 'Perfect.'",
            'escape_attempt': "The narrator: 'Did you really think...?'",
            'enlightened': "The narrator: 'You see it now. All of it.'",
            'betrayed': "The narrator: 'The world is not kind.'",
            'sacrifice': "The narrator: 'Your choice. Your end.'",
        }
        
        return flavors.get(ending_type, "The narrator: '...'")
    
    def get_ending_art(self, ending_type: str) -> str:
        """Get ASCII art for ending type."""
        # Simple patterns for different ending types
        arts = {
            'violent_death': """
        ╔═══════╗
        ║   X   ║
        ╚═══════╝
        """,
            'breakdown': """
        ▓▒░  ?  ░▒▓
        ░▒▓ ??? ▓▒░
        ▓▒░ ??? ░▒▓
        """,
            'merge_am': """
        █████████████
        █ YOU = AM  █
        █████████████
        """,
            'truth_revealed': """
        ╔═══════════╗
        ║    109    ║
        ║  T  E  D  ║
        ╚═══════════╝
        """,
            'transcendence': """
        ★ ═══════ ★
        ║ PERFECT ║
        ★ ═══════ ★
        """,
            'loop_eternal': """
        ∞ ═══════ ∞
        ║  AGAIN  ║
        ∞ ═══════ ∞
        """,
        }
        
        return arts.get(ending_type, """
        ╔═══════╗
        ║  END  ║
        ╚═══════╝
        """)

