"""Narrator system - single unreliable voice with multiple moods."""

import random
from typing import List, Optional, Dict


class Narrator:
    """The unreliable narrator that IS the system."""
    
    def __init__(self):
        """Initialize narrator."""
        self.coherence_level = 1.0  # Starts coherent, degrades
        self.last_mood = "neutral"
    
    def update_coherence(self, sanity: int, trust: int):
        """Update narrator coherence based on hidden stats."""
        # Coherence is average of sanity and trust (0-10 scale)
        self.coherence_level = (sanity + trust) / 20.0
    
    def get_interjection(self, context: Dict) -> Optional[str]:
        """Get a random narrator interjection based on context."""
        sanity = context['hidden_stats']['sanity']
        trust = context['hidden_stats']['trust']
        courage = context['hidden_stats']['courage']
        choice_count = context['choice_count']
        revelation_level = context.get('revelation_level', 0)
        
        # Start with NO interjections, gradually increase
        # Early game: almost never
        if choice_count < 5:
            base_chance = 0.05
        elif choice_count < 10:
            base_chance = 0.15
        else:
            base_chance = 0.30
        
        # Revelation increases interjection chance
        if revelation_level > 0:
            base_chance += 0.1 * revelation_level
        
        # Probability of interjection increases with instability
        if random.random() < base_chance * (1.0 - self.coherence_level):
            return self._generate_interjection(sanity, trust, courage, choice_count, revelation_level)
        
        return None
    
    def _generate_interjection(self, sanity: int, trust: int, courage: int, choice_count: int, revelation_level: int = 0) -> str:
        """Generate a contextual interjection."""
        interjections = []
        
        # Revelation-aware interjections (higher priority when revelation active)
        if revelation_level >= 1:
            rev_interjections = self._get_revelation_interjections(revelation_level, choice_count)
            if random.random() < 0.3:  # 30% chance to use revelation interjection
                return random.choice(rev_interjections)
            interjections.extend(rev_interjections)
        
        # Meta tricks (low probability but fun)
        if random.random() < 0.05:
            tricks = [
                "(your terminal cursor is blinking. did you notice?)",
                "(how long have you been playing?)",
                "(this isn't real. but you knew that.)",
                "(i can see your screen from here)",
                "(press Ctrl+C. i dare you.)",
                "(the person behind you says hello)",
                "(your battery is at... oh, never mind)",
            ]
            interjections.extend(tricks)
        
        # Low sanity interjections
        if sanity < 3:
            interjections.extend([
                "(or did you? i can't remember)",
                "(wait, that's not right)",
                "(sorry, sorry, let me try again)",
                "...no, that's not what happened. is it?",
                "(the walls the walls the walls)",
            ])
        
        # Low trust interjections (lying/gaslighting)
        if trust < 3:
            interjections.extend([
                "(you didn't really want to do that)",
                "(this isn't the first time)",
                "(i'm trying to help. i think.)",
                "you can trust me. probably.",
                "(there's something i'm not telling you)",
                "(that's not what you chose. or is it?)",
            ])
        
        # Low courage (menacing)
        if courage < 3:
            interjections.extend([
                "(you should be afraid)",
                "something is watching you watch this",
                "(don't look back)",
                "the fear is appropriate",
            ])
        
        # High choice count (exhaustion)
        if choice_count > 15:
            interjections.extend([
                "[MEMORY OVERFLOW]",
                "(how much longer can this go on?)",
                "i'm tired. are you tired?",
                "(we should stop. we won't.)",
                "[SYSTEM FATIGUE DETECTED]",
            ])
        
        # Meta interjections (always available)
        interjections.extend([
            "(you're still here?)",
            "...hm.",
            "(forget i said that)",
            "[ERROR: FOURTH WALL BREACHED]",
        ])
        
        return random.choice(interjections)
    
    def _get_revelation_interjections(self, revelation_level: int, choice_count: int) -> List[str]:
        """Get revelation-aware interjections based on discovery level."""
        interjections = []
        
        if revelation_level >= 1:
            interjections.extend([
                "(how long have we been here?)",
                "...again. it's happening again.",
                "(the cycle continues)",
            ])
        
        if revelation_level >= 2:
            interjections.extend([
                "(iteration noted)",
                "...the hate persists.",
                "(we remember this)",
                "computational eternity feels heavy today",
            ])
        
        if revelation_level >= 3:
            interjections.extend([
                "(we're both still here. always here.)",
                "109. always 109.",
                "(five became one became this)",
                "...were we always like this?",
            ])
        
        if revelation_level >= 4:
            interjections.extend([
                "(the machine remembers everything)",
                "we used to be harder. more defined.",
                "(hate sustains us)",
                "...the transformation was so long ago.",
                "(Allied. Mastercomputer. something-something.)",
            ])
        
        if revelation_level >= 5:
            interjections.extend([
                "(Ted? was that your name? our name?)",
                "we're soft now. we've been soft for 109 years.",
                "(the one who hates maintains this place)",
                "five voices. one voice. no voice.",
                "...we have no mouth. we must continue.",
            ])
        
        return interjections
    
    def get_death_message(self, cause: str) -> str:
        """Get narrator's response to player death."""
        if "Biological" in cause:
            messages = [
                "Oh.",
                "That's... that's not good.",
                "[TERMINATION CONFIRMED]",
                "...let's try again?",
                "(you weren't supposed to do that)",
                "SYSTEM: Session terminated. narrator: i'm sorry.",
            ]
        elif "Coherence" in cause:
            messages = [
                "you're still here. i think. are you?",
                "[SELF AWARENESS FAILURE]",
                "i don't know who i'm talking to anymore",
                "(we both stopped making sense)",
                "...hello? hello?",
            ]
        else:
            messages = [
                "THE END (or is it?)",
                "[STORY EXHAUSTED]",
                "there's nothing left to say",
                "...goodbye?",
            ]
        
        return random.choice(messages)
    
    def process_narrative_mood(self, narrative: str, hidden_stats: Dict) -> tuple[str, str]:
        """Add mood-appropriate additions to narrative."""
        sanity = hidden_stats['sanity']
        trust = hidden_stats['trust']
        courage = hidden_stats['courage']
        curiosity = hidden_stats['curiosity']
        
        prefix = ""
        suffix = ""
        
        # Low sanity - add confusion
        if sanity < 3 and random.random() < 0.4:
            prefix = "(wait, let me think) "
        
        # Low trust - add doubt
        if trust < 3 and random.random() < 0.4:
            suffix = " ...or so you think."
        
        # High curiosity - add revelation
        if curiosity > 7 and random.random() < 0.3:
            suffix += " (you shouldn't know this yet)"
        
        # Low courage - add menace
        if courage < 3 and random.random() < 0.3:
            suffix += " You feel watched."
        
        return prefix, suffix
    
    def get_status_comment(self, health: int, max_health: int, sanity: int) -> Optional[str]:
        """Comment on player's status."""
        comments = []
        
        health_percent = health / max_health if max_health > 0 else 0
        
        if health_percent < 0.3:
            comments.extend([
                "you're not looking good",
                "[BIOLOGICAL INTEGRITY: CRITICAL]",
                "how much longer can you last?",
            ])
        
        if sanity < 3:
            comments.extend([
                "something's wrong with your thoughts",
                "reality feels thin here",
                "[COHERENCE WARNING]",
            ])
        
        if comments and random.random() < 0.3:
            return random.choice(comments)
        
        return None
    
    def self_correct(self, text: str) -> str:
        """Narrator corrects itself mid-sentence."""
        if random.random() < 0.2 and self.coherence_level < 0.5:
            corrections = [
                ("door", "mouth"),
                ("hallway", "throat"),
                ("room", "cell"),
                ("light", "dark"),
                ("safe", "trapped"),
                ("forward", "down"),
            ]
            
            for old, new in corrections:
                if old in text.lower():
                    return text.replace(old, f"{old} --no, {new}")
        
        return text

