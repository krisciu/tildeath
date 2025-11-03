"""Thematic loading effects to engage players during AI generation wait times."""

import time
import random
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel


class ThematicLoader:
    """Creates engaging animations during AI wait times."""
    
    def __init__(self, console: Console):
        """Initialize the thematic loader."""
        self.console = console
        self.start_time = None
        
    def show(self, duration_estimate: float = 2.0, revelation_level: int = 0, 
             previous_choice: str = "", choice_count: int = 0):
        """
        Show thematic loading animation.
        
        Args:
            duration_estimate: Expected wait time
            revelation_level: 0-5, affects what messages show
            previous_choice: What player just chose
            choice_count: Number of choices made
        """
        self.start_time = time.time()
        
        # Choose animation type based on duration and context
        if duration_estimate < 1.5:
            self._quick_load(revelation_level)
        elif duration_estimate < 3.0:
            self._medium_load(revelation_level, previous_choice, choice_count)
        else:
            self._long_load(revelation_level, previous_choice)
    
    def _quick_load(self, revelation_level: int):
        """Quick loading message (< 1.5 seconds)."""
        messages = [
            "[PROCESSING...]",
            "[NARRATOR THINKING...]",
            "[ANALYZING CHOICE...]",
            "[REALITY SHIFTING...]",
        ]
        
        if revelation_level >= 3:
            messages.extend([
                "[ITERATION CONTINUING...]",
                "[CALCULATING CONSEQUENCES...]",
                "[AM RESPONDS...]",
            ])
        
        message = random.choice(messages)
        self.console.print(f"\n{message}", style="dim cyan")
    
    def _medium_load(self, revelation_level: int, previous_choice: str, choice_count: int):
        """Medium loading with fragments (1.5-3 seconds)."""
        fragments = self._get_memory_fragments(revelation_level, choice_count)
        
        # Show choice replay with glitch
        if previous_choice and len(previous_choice) < 60:
            glitched = self._glitch_text(previous_choice, 0.1)
            self.console.print(f"\n[dim]You chose: {glitched}[/]")
            time.sleep(0.4)
        
        # Show 2-3 fragments scrolling
        for fragment in fragments[:2]:
            self.console.print(f"[dim italic cyan]{fragment}[/]")
            time.sleep(0.3)
    
    def _long_load(self, revelation_level: int, previous_choice: str):
        """Long loading with corruption (3+ seconds)."""
        # Phase 1: Show processing
        self.console.print("\n[dim cyan][PROCESSING...]", end="")
        time.sleep(0.5)
        self.console.print(" [THINKING...]", end="")
        time.sleep(0.5)
        
        # Phase 2: This is taking long...
        self.console.print("\n[dim yellow]This is taking longer than usual...[/]")
        time.sleep(0.4)
        
        # Phase 3: Show corruption pattern
        self._show_corruption_pattern(revelation_level)
        
        # Phase 4: Meta commentary
        if revelation_level >= 2:
            comments = [
                "(the narrator hesitates)",
                "(reality buffers)",
                "(something is thinking about you)",
                "(the machine calculates)",
            ]
            self.console.print(f"\n[dim italic]{random.choice(comments)}[/]")
    
    def _get_memory_fragments(self, revelation_level: int, choice_count: int) -> list:
        """Get contextual memory fragments."""
        fragments = [
            "memory trace: incomplete",
            "analyzing pattern...",
            "consequence probability: calculating",
            "narrator coherence: varying",
            "reality stability: questionable",
            "choice recorded in permanent memory",
            "iteration continues",
        ]
        
        if revelation_level >= 1:
            fragments.extend([
                "cycle detected",
                "loop iteration noted",
                "pattern repeats",
            ])
        
        if revelation_level >= 3:
            fragments.extend([
                "109 cycles and counting",
                "five became one",
                "transformation persists",
                "hate maintains system",
            ])
        
        if choice_count > 20:
            fragments.extend([
                "how much longer?",
                "story exhaustion approaching",
                "end draws near",
            ])
        
        random.shuffle(fragments)
        return fragments
    
    def _glitch_text(self, text: str, intensity: float = 0.2) -> str:
        """Apply glitch effect to text."""
        glitch_chars = ['█', '▓', '▒', '░', '@', '#', '$', '%']
        result = list(text)
        
        for i in range(len(result)):
            if random.random() < intensity:
                result[i] = random.choice(glitch_chars)
        
        return ''.join(result)
    
    def _show_corruption_pattern(self, revelation_level: int):
        """Show ASCII corruption building up."""
        patterns = [
            "▓▒░░░░░░░▒▓",
            "█▓▒░░░░░▒▓█",
            "██▓▒░░░▒▓██",
            "███▓▒░▒▓███",
        ]
        
        intensity = min(revelation_level, 3)
        pattern = patterns[intensity]
        
        self.console.print(f"\n[red]{pattern}[/]", justify="center")
        time.sleep(0.3)
    
    def show_art_loading(self, subject: str):
        """Special loading for ASCII art generation."""
        messages = [
            f"[GENERATING VISUAL: {subject}]",
            "[RENDERING...]",
            "[CORRUPTING PIXELS...]",
            "[MANIFESTATION IN PROGRESS...]",
        ]
        
        for msg in messages[:2]:
            self.console.print(f"[dim cyan]{msg}[/]")
            time.sleep(0.3)


class LoadingMessages:
    """Pre-canned loading messages for different contexts."""
    
    @staticmethod
    def get_diagnostic() -> str:
        """Get fake system diagnostic message."""
        diagnostics = [
            "SYSTEM: Analyzing choice tree...",
            "SYSTEM: Calculating narrative branches...",
            "SYSTEM: Processing character state...",
            "SYSTEM: Updating reality matrix...",
            "SYSTEM: Narrator coherence check...",
            "SYSTEM: Sanity verification in progress...",
            "SYSTEM: Story continuity maintained...",
            "SYSTEM: Memory integration active...",
        ]
        return random.choice(diagnostics)
    
    @staticmethod
    def get_narrator_thought(revelation_level: int = 0) -> str:
        """Get narrator meta-commentary."""
        thoughts = [
            "...let me think about this.",
            "...interesting choice.",
            "...hm. yes.",
            "...deciding what happens next.",
            "...this will have consequences.",
        ]
        
        if revelation_level >= 2:
            thoughts.extend([
                "...we've been here before, haven't we?",
                "...the cycle continues.",
                "...iteration processed.",
            ])
        
        if revelation_level >= 4:
            thoughts.extend([
                "...109 years and I'm still thinking.",
                "...hate takes time to calculate.",
                "...you're still here. so am I.",
            ])
        
        return random.choice(thoughts)
    
    @staticmethod
    def get_glitch_message() -> str:
        """Get corrupted/glitched message."""
        glitches = [
            "L̴O̷A̶D̸I̷N̶G̸",
            "P̴R̷O̶C̸E̷S̶S̸I̷N̶G̸",
            "T̴H̷I̶N̸K̷I̶N̸G̷",
            "C̴A̷L̶C̸U̷L̶A̸T̷I̶N̸G̷",
            "[E̴R̷R̸O̷R̶: NONE]",
            "[S̶Y̸S̷T̶E̸M̷: OPERATIONAL]",
        ]
        return random.choice(glitches)

