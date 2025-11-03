"""Session management and ghost memory system."""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional


class SessionManager:
    """Manages session state and ghost memory persistence."""
    
    GHOST_FILE = ".ghost_memory"
    
    def __init__(self):
        """Initialize session manager."""
        self.session_start = datetime.now()
        self.ghost_memory = self._load_ghost_memory()
    
    def _load_ghost_memory(self) -> Dict:
        """Load ghost memory from previous sessions."""
        if not os.path.exists(self.GHOST_FILE):
            return {
                "sessions": 0,
                "fragments": [],
                "last_death": None,
                "echoes": [],
                "truth_tracker": {}
            }
        
        try:
            with open(self.GHOST_FILE, 'r') as f:
                data = json.load(f)
                # Ensure truth_tracker key exists
                if 'truth_tracker' not in data:
                    data['truth_tracker'] = {}
                return data
        except Exception:
            # Corrupted ghost memory is thematically appropriate
            return {
                "sessions": "?",
                "fragments": ["[CORRUPTED]"],
                "last_death": "ERROR",
                "echoes": [],
                "truth_tracker": {}
            }
    
    def save_ghost_memory(self, choices: List[str], final_state: Dict, truth_state: Optional[Dict] = None):
        """Save cryptic fragments for next session."""
        # Hash choices to obscure them
        choice_hashes = [hashlib.md5(c.encode()).hexdigest()[:8] for c in choices[-5:]]
        
        # Create cryptic fragments
        fragments = []
        if len(choices) > 0:
            fragments.append(f"trace: {len(choices)} decisions recorded")
        
        if final_state.get('character_stats', {}).get('health', 100) <= 0:
            fragments.append("termination: biological")
        
        # Obscured choice echoes
        echoes = [f"echo_{h}" for h in choice_hashes]
        
        # Get current session count
        current_sessions = self.ghost_memory.get("sessions", 0)
        if isinstance(current_sessions, int):
            new_session_count = current_sessions + 1
        else:
            new_session_count = 1
        
        # Special fragment for session 109
        if new_session_count == 109:
            fragments.append("iteration: 109. subject: still coherent.")
        elif new_session_count > 109:
            fragments.append(f"iteration: {new_session_count}. persistence noted.")
        
        ghost_data = {
            "sessions": new_session_count,
            "fragments": fragments,
            "last_death": datetime.now().isoformat() if final_state.get('character_stats', {}).get('health', 100) <= 0 else None,
            "echoes": echoes,
            "timestamp": datetime.now().isoformat(),
            "truth_tracker": truth_state if truth_state else self.ghost_memory.get("truth_tracker", {})
        }
        
        try:
            with open(self.GHOST_FILE, 'w') as f:
                json.dump(ghost_data, f, indent=2)
        except Exception:
            # If we can't write, that's thematically fine
            pass
    
    def get_opening_memory_hint(self) -> Optional[str]:
        """Get a cryptic hint about previous sessions for the opening."""
        if self.ghost_memory.get("sessions", 0) == 0:
            return None
        
        sessions = self.ghost_memory.get("sessions", 0)
        
        # Special hint for session 109
        if sessions == 109:
            return "iteration: 109. we remember. do you?"
        elif sessions > 109:
            return f"iteration: {sessions}. the cycle continues."
        
        # Helper to get ordinal suffix
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return f"{n}{suffix}"
        
        hints = [
            f"(this is your {ordinal(sessions)} time here. isn't it?)",
            f"[MEMORY TRACE: {sessions} prior session(s) detected]",
            f"you've been here before. {sessions} times. you don't remember.",
            "...have we met?"
        ]
        
        # Return a hint based on session count
        if isinstance(sessions, int) and sessions > 0:
            return hints[min(sessions - 1, len(hints) - 1)]
        
        return None
    
    def get_ghost_fragments(self) -> List[str]:
        """Get fragments from previous sessions."""
        return self.ghost_memory.get("fragments", [])
    
    def session_duration(self) -> float:
        """Get current session duration in seconds."""
        return (datetime.now() - self.session_start).total_seconds()
    
    def get_session_count(self) -> int:
        """Get the current session number."""
        sessions = self.ghost_memory.get("sessions", 0)
        return sessions if isinstance(sessions, int) else 0
    
    def get_truth_state(self) -> Dict:
        """Get saved truth tracker state."""
        return self.ghost_memory.get("truth_tracker", {})

