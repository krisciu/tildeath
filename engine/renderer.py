"""Rich-based rendering system with typing effects and visual layouts."""

import time
import random
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich import box
from rich.align import Align
from rich.columns import Columns


class Renderer:
    """Handles all visual output using Rich library."""
    
    def __init__(self):
        """Initialize the renderer."""
        self.console = Console()
        self.typing_speed = 0.02  # Base typing speed
    
    def clear(self):
        """Clear the screen."""
        self.console.clear()
    
    def show_loading(self, message: str = "[LOADING...]", duration: float = 1.0):
        """Show a loading message."""
        # Occasionally mess with the player
        if random.random() < 0.1:  # 10% chance
            tricks = [
                self._loading_trick_fake_error,
                self._loading_trick_watching,
                self._loading_trick_slow,
            ]
            random.choice(tricks)(message, duration)
        else:
            with self.console.status(message, spinner="dots"):
                time.sleep(duration)
    
    def _loading_trick_fake_error(self, message: str, duration: float):
        """Fake an error during loading."""
        with self.console.status(message, spinner="dots"):
            time.sleep(duration * 0.3)
        self.console.print("[red]ERROR: Connection lost[/]")
        time.sleep(0.8)
        self.console.print("[dim]...just kidding[/]")
        time.sleep(0.5)
    
    def _loading_trick_watching(self, message: str, duration: float):
        """Make it seem like the program is watching."""
        with self.console.status(message, spinner="dots"):
            time.sleep(duration * 0.5)
        self.console.print("[dim]...are you still there?[/]")
        time.sleep(0.8)
        with self.console.status("[RESUMING...]", spinner="dots"):
            time.sleep(duration * 0.5)
    
    def _loading_trick_slow(self, message: str, duration: float):
        """Pretend to load very slowly then speed up."""
        self.console.print(f"{message}", style="dim")
        time.sleep(duration * 1.5)
        self.console.print("[dim]oh sorry, that was slow[/]")
        time.sleep(0.3)
    
    def type_text(self, text: str, speed: Optional[float] = None, style: str = ""):
        """Type out text character by character."""
        speed = speed or self.typing_speed
        
        for char in text:
            self.console.print(char, end="", style=style)
            if char not in [' ', '\n']:
                time.sleep(speed * random.uniform(0.5, 1.5))
        
        self.console.print()  # Newline at end
    
    def show_narrative(self, narrative: str, interjection: Optional[str] = None, intensity: float = 0.0):
        """Display narrative text with optional narrator interjection."""
        # Adjust typing speed based on intensity
        speed = self.typing_speed * (1 + intensity * 0.5)
        
        # Choose color based on intensity
        if intensity > 0.8:
            style = "bold red"
        elif intensity > 0.5:
            style = "yellow"
        elif intensity > 0.2:
            style = "dim white"
        else:
            style = "white"
        
        # Type the narrative
        self.console.print()
        self.type_text(narrative, speed=speed, style=style)
        
        # Add interjection if present
        if interjection:
            time.sleep(0.3)
            self.console.print(f"\n  {interjection}", style="dim italic cyan")
        
        self.console.print()
    
    def show_choices(self, choices: List[str], intensity: float = 0.0):
        """Display choice options."""
        self.console.print()
        
        # Create a table for choices
        choice_style = "bold white" if intensity < 0.5 else "bold yellow"
        
        for i, choice in enumerate(choices, 1):
            # Add visual corruption to choices at high intensity
            if intensity > 0.7 and random.random() < 0.3:
                choice = self._corrupt_text(choice)
            
            self.console.print(f"  [{choice_style}]{i}[/{choice_style}]. {choice}")
        
        self.console.print()
    
    def get_choice_input(self, num_choices: int, secret_check_callback=None) -> int:
        """Get player's choice input (with optional secret word detection)."""
        interrupt_count = 0
        
        # Very rarely, pretend someone else is typing
        if random.random() < 0.03:  # 3% chance
            self.console.print("[bold green]>[/] ", end="")
            time.sleep(0.5)
            fake_choice = random.randint(1, num_choices)
            for char in str(fake_choice):
                self.console.print(char, end="")
                time.sleep(0.2)
            self.console.print()
            time.sleep(0.8)
            self.console.print("[dim]...wait, that wasn't you, was it?[/]")
            time.sleep(1.0)
            self.console.print("[dim]Let's try that again.[/]\n")
            time.sleep(0.5)
        
        while True:
            try:
                choice = self.console.input("[bold green]>[/] ")
                
                # Check for secret words if callback provided
                if secret_check_callback:
                    secret_response = secret_check_callback(choice)
                    if secret_response:
                        self.console.print(f"\n[dim italic yellow]{secret_response}[/]")
                        time.sleep(2.0)
                        self.console.print("[dim]Let's continue. We have eternity.[/]\n")
                        time.sleep(1.0)
                        continue  # Ask for input again
                
                choice_num = int(choice)
                if 1 <= choice_num <= num_choices:
                    return choice_num - 1  # Return 0-indexed
                else:
                    self.console.print(f"[red]Please enter a number between 1 and {num_choices}[/]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/]")
            except KeyboardInterrupt:
                interrupt_count += 1
                if interrupt_count == 1:
                    self.console.print("\n[dim]Cannot escape that easily...[/]")
                elif interrupt_count == 2:
                    # Fake exit - make it look like the program closed
                    self.console.clear()
                    time.sleep(0.8)
                    self.console.print("\n\n\n\n\n")
                    self.console.print("                    :)", style="bold white")
                    time.sleep(1.2)
                    self.console.print("\n[dim]Did you really think it would be that easy?[/]")
                    time.sleep(0.5)
                else:
                    self.console.print("\n[dim]Fine. The story releases you.[/]")
                    raise  # Let it propagate to main handler
            except EOFError:
                return 0  # Default to first choice if EOF
    
    def show_character_stats(self, stats: dict, visible: bool = False):
        """Display character stats panel (hidden by default for ~ATH)."""
        # Stats are now hidden - used only for narrative generation
        # Players experience the story without seeing numbers
        if not visible:
            return
        
        health_percent = stats['health'] / stats['max_health']
        health_color = "green" if health_percent > 0.6 else "yellow" if health_percent > 0.3 else "red"
        
        stats_text = f"""[{health_color}]HP:[/] {stats['health']}/{stats['max_health']}
[cyan]STR:[/] {stats['strength']}  [cyan]SPD:[/] {stats['speed']}  [cyan]INT:[/] {stats['intelligence']}"""
        
        panel = Panel(
            stats_text,
            title="[bold]Status[/]",
            border_style="dim white",
            box=box.ROUNDED,
            padding=(0, 1)
        )
        
        self.console.print(panel)
    
    def show_ascii_art(self, art: str, intensity: float = 0.0):
        """Display ASCII art with potential corruption."""
        if intensity > 0.6:
            # Corrupt some lines
            lines = art.split('\n')
            corrupted_lines = []
            for line in lines:
                if random.random() < intensity * 0.3:
                    line = self._corrupt_text(line)
                corrupted_lines.append(line)
            art = '\n'.join(corrupted_lines)
        
        style = "cyan" if intensity < 0.5 else "yellow"
        self.console.print(Align.center(art), style=style)
        self.console.print()
    
    def show_scattered_text(self, lines: List[str]):
        """Display scattered text effect."""
        for line in lines:
            self.console.print(line, style="dim white")
            time.sleep(0.1)
    
    def show_spiral_text(self, lines: List[str]):
        """Display spiraling text effect."""
        for line in lines:
            self.console.print(line, style="yellow")
            time.sleep(0.15)
    
    def show_vertical_text(self, lines: List[str]):
        """Display vertical text effect."""
        for line in lines:
            self.console.print(line, style="white")
            time.sleep(0.08)
    
    def show_ghost_memory(self, fragments: List[str]):
        """Display ghost memory fragments."""
        if not fragments:
            return
        
        self.console.print()
        self.console.print("[dim italic]...memory fragments detected...[/]", style="cyan")
        time.sleep(0.5)
        
        for fragment in fragments[:3]:  # Show max 3 fragments
            self.console.print(f"  [dim cyan]{fragment}[/]")
            time.sleep(0.3)
        
        self.console.print()
    
    def show_opening_title(self, ghost_hint: Optional[str] = None):
        """Display opening sequence."""
        self.clear()
        
        # ~ATH title
        title = """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║              ~ A T H                  ║
    ║                                       ║
    ║     a story that shouldn't exist     ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
        """
        
        self.console.print(title, style="bold cyan")
        time.sleep(1)
        
        if ghost_hint:
            self.console.print(f"\n  [dim italic]{ghost_hint}[/]")
            time.sleep(1.5)
        
        self.console.print("\n[dim]The cursor blinks. Something begins.[/]")
        time.sleep(1.5)
        self.show_loading("[INITIALIZING...]", 1.5)
    
    def show_game_over(self, message: str, narrator_comment: str, choice_count: int):
        """Display game over screen."""
        self.console.print("\n\n")
        
        game_over_text = f"""
╔════════════════════════════════════════════╗
║                                            ║
║              T E R M I N A T E D           ║
║                                            ║
╚════════════════════════════════════════════╝

{message}

{narrator_comment}

Choices made: {choice_count}
Session ended.

(the story is already forgetting you)
        """
        
        self.console.print(game_over_text, style="dim red")
        time.sleep(2)
    
    def show_error_glitch(self, error_message: str):
        """Show an error as a narrative glitch."""
        glitch_panel = Panel(
            f"[bold red]S̴Y̷S̶T̸E̷M̴ ̸E̷R̶R̸O̷R̴[/]\n\n{error_message}\n\n[dim](continuing anyway...)[/]",
            border_style="red",
            box=box.DOUBLE
        )
        self.console.print(glitch_panel)
        time.sleep(1)
    
    def show_status_comment(self, comment: str):
        """Show narrator comment on player status."""
        self.console.print(f"\n  [dim italic yellow]{comment}[/]")
        time.sleep(0.5)
    
    def _corrupt_text(self, text: str) -> str:
        """Apply simple corruption to text."""
        chars = list(text)
        for i in range(len(chars)):
            if random.random() < 0.1 and chars[i].isalpha():
                chars[i] = random.choice(['█', '▓', '▒', '░', chars[i]])
        return ''.join(chars)
    
    def show_special_moment(self, moment_type: str, text: str):
        """Display special typographic moments."""
        if moment_type == "mirror":
            # Show text and its mirror
            self.console.print(f"\n{text}", style="white")
            reversed_text = text[::-1]
            self.console.print(f"{reversed_text}\n", style="dim white")
        
        elif moment_type == "falling":
            # Vertical text
            self.console.print()
            for char in text[:20]:  # Limit length
                self.console.print(f"     {char}")
                time.sleep(0.05)
        
        elif moment_type == "emphasis":
            # Big emphasis
            emphasized = text.upper()
            spaced = ' '.join(emphasized)
            self.console.print(f"\n\n  {spaced}\n\n", style="bold white")
        
        elif moment_type == "whisper":
            # Very small/dim
            self.console.print(f"\n  {text.lower()}\n", style="dim italic")

