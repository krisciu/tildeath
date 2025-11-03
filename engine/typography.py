"""Typography and visual effects system - House of Leaves inspired."""

import random
import re
from typing import List
from config.settings import VISUAL_INTENSITY


class TypographyEngine:
    """Handles experimental text layout and visual effects."""
    
    # Unicode characters for corruption effects
    CORRUPTION_CHARS = ['̴', '̷', '̶', '̸', '̵', '̢', '̡', '̧', '̨', '̛']
    GLITCH_REPLACEMENTS = {
        'a': ['@', 'a', '4'],
        'e': ['3', 'e', 'é'],
        'i': ['1', 'i', '!'],
        'o': ['0', 'o', 'ø'],
        's': ['$', '5', 's'],
        't': ['+', 't', '7'],
    }
    
    def __init__(self):
        """Initialize typography engine."""
        self.intensity = 0.0
    
    def set_intensity(self, intensity_level: str):
        """Set visual intensity based on game state."""
        self.intensity = VISUAL_INTENSITY.get(intensity_level, 0.0)
    
    def apply_effects(self, text: str, intensity_override: float = None) -> str:
        """Apply typography effects based on current intensity."""
        intensity = intensity_override if intensity_override is not None else self.intensity
        
        if intensity <= 0.1:
            # Even when stable, occasionally mess with the player
            if random.random() < 0.02:  # 2% chance
                return self._add_meta_trick(text)
            return text  # No effects when stable
        
        # Apply effects with increasing probability
        effects = []
        
        if random.random() < intensity * 0.3:
            text = self._add_spacing_glitches(text, intensity)
        
        if random.random() < intensity * 0.4:
            text = self._add_character_substitution(text, intensity)
        
        if random.random() < intensity * 0.25:
            text = self._add_repetition(text, intensity)
        
        if intensity > 0.5 and random.random() < intensity * 0.2:
            text = self._add_corruption(text, intensity)
        
        return text
    
    def _add_meta_trick(self, text: str) -> str:
        """Add subtle meta tricks even when stable."""
        tricks = [
            lambda t: t + " (wait, did I say that out loud?)",
            lambda t: t.replace("you", "you (yes, you reading this)"),
            lambda t: "[RECORDING] " + t,
            lambda t: t + " [REDACTED]",
        ]
        return random.choice(tricks)(text)
    
    def _add_spacing_glitches(self, text: str, intensity: float) -> str:
        """Add random spacing issues."""
        words = text.split()
        result = []
        
        for word in words:
            if random.random() < intensity * 0.3:
                # Add extra spaces within word
                chars = list(word)
                spaced = ' '.join(chars) if len(chars) > 3 else word
                result.append(spaced)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _add_character_substitution(self, text: str, intensity: float) -> str:
        """Replace characters with glitch alternatives."""
        result = []
        
        for char in text:
            if char.lower() in self.GLITCH_REPLACEMENTS and random.random() < intensity * 0.15:
                replacements = self.GLITCH_REPLACEMENTS[char.lower()]
                result.append(random.choice(replacements))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _add_repetition(self, text: str, intensity: float) -> str:
        """Add word/syllable repetition."""
        words = text.split()
        result = []
        
        for word in words:
            if random.random() < intensity * 0.2 and len(word) > 3:
                # Repeat the word or stutter it
                if random.random() < 0.5:
                    result.append(f"{word} {word}")
                else:
                    # Stutter first syllable
                    stutter = word[:2] + '-' + word
                    result.append(stutter)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _add_corruption(self, text: str, intensity: float) -> str:
        """Add Unicode corruption marks."""
        result = []
        
        for char in text:
            result.append(char)
            if char.isalpha() and random.random() < intensity * 0.1:
                result.append(random.choice(self.CORRUPTION_CHARS))
        
        return ''.join(result)
    
    def create_scattered_text(self, text: str, width: int = 80) -> List[str]:
        """Scatter text across multiple lines (panic effect)."""
        words = text.split()
        lines = [''] * 10
        
        for word in words:
            line_idx = random.randint(0, len(lines) - 1)
            pos = random.randint(0, max(0, width - len(word) - 1))
            
            # Create spacing
            spaced_word = ' ' * pos + word
            if len(lines[line_idx]) < pos:
                lines[line_idx] = lines[line_idx].ljust(pos) + word
            else:
                lines[line_idx] += '  ' + word
        
        return [line for line in lines if line.strip()]
    
    def create_spiral_text(self, text: str, inward: bool = True) -> List[str]:
        """Create spiraling text effect."""
        words = text.split()
        lines = []
        indent = 0 if inward else 20
        
        for i, word in enumerate(words[:8]):  # Limit for readability
            if inward:
                indent = i * 2
            else:
                indent = max(0, 20 - i * 2)
            
            lines.append(' ' * indent + word)
        
        return lines
    
    def create_vertical_text(self, text: str) -> List[str]:
        """Create vertical text (falling/climbing effect)."""
        words = text.split()[:5]  # Limit words
        lines = []
        
        for word in words:
            for char in word:
                lines.append('    ' + char)
        
        return lines
    
    def add_strikethrough(self, text: str, word_to_strike: str) -> str:
        """Add strikethrough effect to specific words using Unicode."""
        # Use Unicode strikethrough combining character
        struck = ''.join(c + '\u0336' for c in word_to_strike)
        return text.replace(word_to_strike, struck)
    
    def add_marginalia(self, text: str, note: str, position: str = 'end') -> str:
        """Add margin notes/asides."""
        if position == 'end':
            return f"{text}  [{note}]"
        elif position == 'start':
            return f"[{note}]  {text}"
        else:  # middle
            words = text.split()
            mid = len(words) // 2
            words.insert(mid, f"[{note}]")
            return ' '.join(words)
    
    def create_size_emphasis(self, text: str, emphasis_word: str) -> str:
        """Emphasize words with visual sizing (limited in terminal)."""
        # Use spacing and caps to simulate size
        emphasized = emphasis_word.upper()
        spaced = ' '.join(emphasized)
        return text.replace(emphasis_word, f"\n  {spaced}\n")
    
    def create_fake_footnote(self) -> str:
        """Create fake footnote markers."""
        footnotes = [
            "[1] There is no footnote 1.",
            "[*] This note leads nowhere.",
            "[?] You shouldn't read this.",
            "[†] [MISSING]"
        ]
        return random.choice(footnotes)
    
    def process_narrator_corrections(self, text: str) -> str:
        """Process strikethrough corrections in text."""
        # Look for patterns like "safe" that should be "trapped"
        patterns = [
            ("safe", "trapped"),
            ("door", "mouth"),
            ("hallway", "throat"),
            ("room", "stomach"),
            ("exit", "entrance"),
            ("forward", "backward"),
        ]
        
        if random.random() < self.intensity * 0.3:
            old, new = random.choice(patterns)
            if old in text.lower():
                # Use Unicode strikethrough
                struck_old = ''.join(c + '\u0336' for c in old)
                text = re.sub(
                    r'\b' + old + r'\b', 
                    f"{struck_old} {new}", 
                    text, 
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return text
    
    def get_loading_glitch(self) -> str:
        """Get a loading message that fits the aesthetic."""
        messages = [
            "[LOADING...]",
            "[REMEMBERING...]",
            "[FORGETTING...]",
            "[RECONSTRUCTING...]",
            "[C̴O̷N̶N̸E̷C̴T̸I̷N̶G̸...]",
            "[PLEASE WAIT]",
            "[DO NOT WAIT]",
            "[T̷I̶M̸E̷ ̶E̸R̷R̶O̷R̴]",
        ]
        
        if self.intensity > 0.5:
            return random.choice(messages[-4:])
        return random.choice(messages[:4])

