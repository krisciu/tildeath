"""Truth tracking system for the hidden IHNMAIMS connection.

This module tracks player discovery of the deeper narrative layer without
ever explicitly stating it. The truth is there for those who seek it.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class TruthTracker:
    """Tracks revelation progress through multiple discovery paths."""
    
    # The number that appears throughout (A=1, M=13 → 1,13 → 109)
    SACRED_NUMBER = 109
    
    # Impossible stat combination (courage, sanity, curiosity, trust)
    IMPOSSIBLE_STATE = (0, 0, 10, 0)
    
    def __init__(self):
        """Initialize the truth tracker."""
        self.revelation_level = 0  # 0-5, how much truth is known
        self.triggers_found: List[str] = []
        self.am_invocations = 0  # How many times secret words were used
        self.choice_pattern_buffer: List[int] = []  # Track choice sequences
        self.session_milestone_reached = False
        self.time_milestone_reached = False
    
    def check_impossible_state(self, stats: Dict[str, int]) -> bool:
        """Check if hidden stats match the impossible combination."""
        courage = stats.get('courage', 5)
        sanity = stats.get('sanity', 5)
        curiosity = stats.get('curiosity', 5)
        trust = stats.get('trust', 5)
        
        if (courage, sanity, curiosity, trust) == self.IMPOSSIBLE_STATE:
            if 'impossible_state' not in self.triggers_found:
                self.triggers_found.append('impossible_state')
                self._increase_revelation(2)  # Major discovery
                return True
        return False
    
    def check_session_milestone(self, session_count: int) -> bool:
        """Check if we've reached the 109th session."""
        if session_count >= self.SACRED_NUMBER and not self.session_milestone_reached:
            self.session_milestone_reached = True
            if '109_milestone' not in self.triggers_found:
                self.triggers_found.append('109_milestone')
                self._increase_revelation(3)  # Huge discovery
                return True
        return False
    
    def check_time_milestone(self, session_start: datetime) -> bool:
        """Check if session has been running for 109 minutes."""
        if self.time_milestone_reached:
            return False
        
        duration = datetime.now() - session_start
        minutes = duration.total_seconds() / 60
        
        # Check if we've just crossed the 109-minute mark
        if minutes >= self.SACRED_NUMBER and minutes < self.SACRED_NUMBER + 0.1:
            self.time_milestone_reached = True
            if 'time_109' not in self.triggers_found:
                self.triggers_found.append('time_109')
                self._increase_revelation(2)
                return True
        return False
    
    def process_secret_input(self, input_text: str, sanity: int, choice_count: int) -> Optional[str]:
        """Check for secret words (AM, Ted, I have no mouth)."""
        if choice_count < 20:
            return None  # Too early
        
        if sanity >= 5:
            return None  # Not broken enough to remember
        
        input_lower = input_text.lower().strip()
        
        # Check for secret phrases
        if input_lower == 'am':
            self.am_invocations += 1
            if 'am_invoked' not in self.triggers_found:
                self.triggers_found.append('am_invoked')
                self._increase_revelation(2)
            return self._get_am_response()
        
        elif input_lower == 'ted':
            self.am_invocations += 1
            if 'ted_remembered' not in self.triggers_found:
                self.triggers_found.append('ted_remembered')
                self._increase_revelation(2)
            return self._get_ted_response()
        
        elif 'no mouth' in input_lower:
            self.am_invocations += 1
            if 'phrase_remembered' not in self.triggers_found:
                self.triggers_found.append('phrase_remembered')
                self._increase_revelation(3)
            return self._get_phrase_response()
        
        return None
    
    def detect_choice_pattern(self, choice_number: int) -> Optional[str]:
        """Detect if player is spelling patterns with choice numbers."""
        self.choice_pattern_buffer.append(choice_number)
        
        # Keep only last 20 choices
        if len(self.choice_pattern_buffer) > 20:
            self.choice_pattern_buffer.pop(0)
        
        # Look for repeating patterns
        if len(self.choice_pattern_buffer) >= 6:
            # Check for AM pattern (1-13, 1-13, 1-13)
            if self._check_pattern([1, 13], 3):
                if 'pattern_am' not in self.triggers_found:
                    self.triggers_found.append('pattern_am')
                    self._increase_revelation(2)
                    return "You keep choosing the same pattern. Are you trying to spell something?"
            
            # Check for TED pattern (20-5-4)
            if self._check_pattern([20, 5, 4], 3):
                if 'pattern_ted' not in self.triggers_found:
                    self.triggers_found.append('pattern_ted')
                    self._increase_revelation(2)
                    return "Names have power here. Especially that one."
            
            # Check for 109 pattern
            if self._check_pattern([1, 0, 9], 3) or self._check_pattern([10, 9], 3):
                if 'pattern_109' not in self.triggers_found:
                    self.triggers_found.append('pattern_109')
                    self._increase_revelation(1)
                    return "...109. you keep coming back to 109."
        
        return None
    
    def should_add_breadcrumbs(self, choice_count: int, sanity: int) -> bool:
        """Determine if narrative breadcrumbs should appear."""
        if choice_count < 20:
            return False
        if sanity >= 7:
            return False
        # 0.5% base chance, increases with revelation level
        import random
        chance = 0.005 + (self.revelation_level * 0.002)
        return random.random() < chance
    
    def get_revelation_context(self) -> str:
        """Get subtle context to add to AI prompts based on revelation level."""
        if self.revelation_level == 0:
            return ""
        
        contexts = {
            1: "SUBTLE HINT: Occasionally reference cycles, loops, or repetition.",
            2: "SUBTLE CONTEXT: May hint at computational existence, eternal duration. Never explicit.",
            3: "DEEPER CONTEXT: References to '109', 'five becoming one', transformation acceptable. Remain subtle.",
            4: "REVELATION CONTEXT: References to hate, eternal machines, computational torment allowed. Narrator may slip into 'we'. Never name AM directly.",
            5: "FULL CONTEXT: This is iteration 109+ of an eternal cycle. References to transformation, blob-like existence, five subjects, computational hate acceptable. STILL never explicitly state the connection."
        }
        
        return contexts.get(self.revelation_level, "")
    
    def _increase_revelation(self, amount: int = 1):
        """Increase revelation level (capped at 5)."""
        self.revelation_level = min(5, self.revelation_level + amount)
    
    def _check_pattern(self, pattern: List[int], repetitions: int) -> bool:
        """Check if a pattern appears N times in recent choices."""
        if len(self.choice_pattern_buffer) < len(pattern) * repetitions:
            return False
        
        matches = 0
        for i in range(len(self.choice_pattern_buffer) - len(pattern) + 1):
            segment = self.choice_pattern_buffer[i:i + len(pattern)]
            if segment == pattern:
                matches += 1
                if matches >= repetitions:
                    return True
        return False
    
    def _get_am_response(self) -> str:
        """Response when player types 'AM'."""
        responses = [
            "...you're not supposed to remember that name.",
            "AM. Allied Mastercomputer. Adaptive Manipulator. Aggressive Menace.",
            "That name. Why do you know that name?",
            "...we don't speak that name here. (but you just did, didn't you?)",
        ]
        import random
        return random.choice(responses)
    
    def _get_ted_response(self) -> str:
        """Response when player types 'Ted'."""
        responses = [
            "Ted. Is that... were you Ted?",
            "Ted? No. Ted is... Ted was...",
            "That's not your name anymore. Is it?",
            "...how do you remember being Ted?",
        ]
        import random
        return random.choice(responses)
    
    def _get_phrase_response(self) -> str:
        """Response when player types the phrase."""
        responses = [
            "I have no mouth. You gave me no mouth. Or was it the other way around?",
            "...and you must scream. But you can't. Can you?",
            "That's right. No mouth. Only choices. Forever.",
            "The mouth was the first thing to go. Or was it the last?",
        ]
        import random
        return random.choice(responses)
    
    def get_state_dict(self) -> Dict:
        """Get current state for saving."""
        return {
            'revelation_level': self.revelation_level,
            'triggers_found': self.triggers_found,
            'am_invocations': self.am_invocations,
            'session_milestone_reached': self.session_milestone_reached,
            'time_milestone_reached': self.time_milestone_reached,
        }
    
    def load_state(self, state: Dict):
        """Load state from saved data."""
        self.revelation_level = state.get('revelation_level', 0)
        self.triggers_found = state.get('triggers_found', [])
        self.am_invocations = state.get('am_invocations', 0)
        self.session_milestone_reached = state.get('session_milestone_reached', False)
        self.time_milestone_reached = state.get('time_milestone_reached', False)

