#!/usr/bin/env python3
"""
Visual effects demonstration - no API required.
Run this to see the typography engine in action.
"""

from engine.renderer import Renderer
from engine.typography import TypographyEngine
import time

def main():
    renderer = Renderer()
    typo = TypographyEngine()
    
    renderer.clear()
    renderer.console.print("\n[bold cyan]Terminal Story Engine - Visual Effects Demo[/]\n")
    time.sleep(1)
    
    # Test 1: Typing effect
    renderer.console.print("[bold]1. Typing Effect:[/]")
    renderer.type_text("This text appears character by character, like someone is typing it...", speed=0.03)
    time.sleep(1)
    
    # Test 2: Progressive corruption
    renderer.console.print("\n[bold]2. Progressive Text Corruption:[/]")
    base_text = "The door stands before you, waiting."
    
    for intensity_name in ['stable', 'unsettled', 'disturbed', 'breaking', 'collapsed']:
        typo.set_intensity(intensity_name)
        corrupted = typo.apply_effects(base_text)
        renderer.console.print(f"  [{intensity_name}]: {corrupted}")
        time.sleep(0.8)
    
    # Test 3: Narrator corrections
    renderer.console.print("\n[bold]3. Narrator Self-Corrections:[/]")
    typo.set_intensity('disturbed')
    text = "You walk down the safe hallway toward the exit door."
    corrected = typo.process_narrator_corrections(text)
    renderer.console.print(f"  {corrected}")
    time.sleep(1.5)
    
    # Test 4: Scattered text (panic)
    renderer.console.print("\n[bold]4. Scattered Text (Panic Effect):[/]")
    scattered = typo.create_scattered_text("Everything breaks apart you cannot hold the pieces", width=60)
    renderer.show_scattered_text(scattered)
    time.sleep(1.5)
    
    # Test 5: Spiral text
    renderer.console.print("\n[bold]5. Spiraling Text (Paranoia Effect):[/]")
    spiral = typo.create_spiral_text("Deeper and deeper into the spiral you go without return", inward=True)
    renderer.show_spiral_text(spiral)
    time.sleep(1.5)
    
    # Test 6: Marginalia
    renderer.console.print("\n[bold]6. Marginalia (Hidden Notes):[/]")
    text_with_note = typo.add_marginalia("The narrator says you're safe", "this is a lie", "end")
    renderer.console.print(f"  {text_with_note}")
    time.sleep(1)
    
    # Test 7: Fake footnotes
    renderer.console.print("\n[bold]7. Fake Footnotes:[/]")
    footnote = typo.create_fake_footnote()
    renderer.console.print(f"  See reference{footnote}")
    time.sleep(1)
    
    # Test 8: Loading glitches
    renderer.console.print("\n[bold]8. Loading Messages:[/]")
    for _ in range(3):
        typo.set_intensity(['stable', 'disturbed', 'collapsed'][_])
        message = typo.get_loading_glitch()
        renderer.show_loading(message, 0.8)
    
    # Test 9: Special moments
    renderer.console.print("\n[bold]9. Special Typographic Moments:[/]")
    
    renderer.console.print("\n  [cyan]Mirror effect:[/]")
    renderer.show_special_moment("mirror", "REDRUM")
    time.sleep(1)
    
    renderer.console.print("  [cyan]Emphasis:[/]")
    renderer.show_special_moment("emphasis", "RUN")
    time.sleep(1)
    
    renderer.console.print("  [cyan]Whisper:[/]")
    renderer.show_special_moment("whisper", "can you hear me?")
    time.sleep(1)
    
    # Test 10: Character stats display
    renderer.console.print("\n[bold]10. Character Stats Panel:[/]")
    test_stats = {
        'health': 45,
        'max_health': 100,
        'strength': 7,
        'speed': 4,
        'intelligence': 6
    }
    renderer.show_character_stats(test_stats)
    time.sleep(1)
    
    # Test 11: Narrative with interjection
    renderer.console.print("\n[bold]11. Narrative with Narrator Interjection:[/]")
    typo.set_intensity('disturbed')
    test_narrative = "You open the ancient book. The pages are blank, yet somehow you can read them."
    renderer.show_narrative(test_narrative, "(that doesn't make sense, does it?)", intensity=0.5)
    time.sleep(1)
    
    # Test 12: Choices display
    renderer.console.print("[bold]12. Choice Display:[/]")
    test_choices = [
        "Trust the narrator",
        "Question everything",
        "Look for an exit",
        "Embrace the void"
    ]
    renderer.show_choices(test_choices, intensity=0.3)
    
    # Outro
    renderer.console.print("\n[dim]Visual effects demonstration complete.[/]")
    renderer.console.print("[dim]Run 'python main.py' with a valid API key to play the full game.[/]\n")


if __name__ == "__main__":
    main()

