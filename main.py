#!/usr/bin/env python3
"""
Terminal Story Engine - A reality-bending CYOA experience.

The story begins when you run this file. There is no menu. No pause.
The terminal becomes the story, and the story knows it's being told.
"""

import sys
import os
import random
import time
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from engine.story_engine import StoryEngine
from engine.ai_adapter import AIAdapter
from engine.narrator import Narrator
from engine.renderer import Renderer
from engine.typography import TypographyEngine
from engine.session import SessionManager
from engine.truth_tracker import TruthTracker
from config.prompts import get_revelation_modifiers


class Game:
    """Main game controller."""
    
    def __init__(self):
        """Initialize all game systems."""
        try:
            self.story = StoryEngine()
            self.ai = AIAdapter()
            self.narrator = Narrator()
            self.renderer = Renderer()
            self.typography = TypographyEngine()
            self.session = SessionManager()
            self.truth = TruthTracker()
            
            # Load truth state from ghost memory
            truth_state = self.session.get_truth_state()
            if truth_state:
                self.truth.load_state(truth_state)
        except ValueError as e:
            print(f"\nERROR: {e}")
            print("\nPlease create a .env file with your ANTHROPIC_API_KEY")
            print("Example: ANTHROPIC_API_KEY=sk-ant-...")
            sys.exit(1)
    
    def run(self):
        """Run the game loop."""
        try:
            # Opening sequence
            ghost_hint = self.session.get_opening_memory_hint()
            self.renderer.show_opening_title(ghost_hint)
            
            # Show ghost memory fragments if they exist
            fragments = self.session.get_ghost_fragments()
            if fragments:
                self.renderer.show_ghost_memory(fragments)
            
            # Generate opening scene
            self.renderer.show_loading(self.typography.get_loading_glitch(), 1.5)
            opening = self.ai.generate_opening()
            
            if not opening.get('error'):
                self.story.set_narrative(opening['narrative'])
            
            # Check for session 109 milestone
            session_count = self.session.get_session_count()
            if self.truth.check_session_milestone(session_count):
                self.renderer.console.print("\n[dim italic]iteration: 109. we remember.[/]")
                time.sleep(2.0)
            
            # Main game loop
            while True:
                # Check for game over
                is_over, death_message = self.story.is_game_over()
                if is_over:
                    narrator_comment = self.narrator.get_death_message(death_message)
                    self.renderer.show_game_over(
                        death_message, 
                        narrator_comment, 
                        self.story.choice_count
                    )
                    break
                
                # Get current context
                context = self.story.get_context()
                visual_intensity = context['visual_intensity']
                
                # Check truth tracker milestones
                # 1. Check impossible state
                if self.truth.check_impossible_state(context['hidden_stats']):
                    self.renderer.console.print("\n[dim italic red]...something shifts in your awareness...[/]")
                    time.sleep(1.5)
                
                # 2. Check 109-minute session
                if self.truth.check_time_milestone(self.session.session_start):
                    self.renderer.console.print("\n\n[bold red]...109 minutes. always 109.[/]")
                    time.sleep(1.5)
                    self.renderer.console.print("[dim]How long have we been here, exactly?[/]")
                    time.sleep(1.5)
                
                # 3. Add revelation level to context
                context['revelation_level'] = self.truth.revelation_level
                
                # Update systems
                self.typography.set_intensity(visual_intensity)
                self.narrator.update_coherence(
                    context['hidden_stats']['sanity'],
                    context['hidden_stats']['trust']
                )
                
                # Display narrative (always use opening which contains current AI response)
                narrative = opening.get('narrative', '')
                if not narrative:
                    narrative = "The space around you shifts. Reality feels negotiable."
                
                # Apply typography effects
                narrative = self.typography.apply_effects(narrative)
                narrative = self.typography.process_narrator_corrections(narrative)
                
                # Add narrator mood
                prefix, suffix = self.narrator.process_narrative_mood(
                    narrative, 
                    context['hidden_stats']
                )
                narrative = prefix + narrative + suffix
                
                # Get narrator interjection (revelation-aware)
                interjection = self.narrator.get_interjection(context)
                
                # Check if breadcrumbs should appear
                breadcrumb_active = self.truth.should_add_breadcrumbs(
                    context['choice_count'],
                    context['hidden_stats']['sanity']
                )
                
                # Calculate intensity for rendering
                intensity = self.typography.intensity
                
                # Character stats are hidden - used only for narrative generation
                # self.renderer.show_character_stats(context['character_stats'])
                
                # Show narrative with effects
                self.renderer.show_narrative(narrative, interjection, intensity)
                
                # Occasional status comment from narrator
                status_comment = self.narrator.get_status_comment(
                    context['character_stats']['health'],
                    context['character_stats']['max_health'],
                    context['hidden_stats']['sanity']
                )
                if status_comment:
                    self.renderer.show_status_comment(status_comment)
                
                # Show choices (always use opening which contains current AI response)
                choices = opening.get('choices', [])
                if not choices or len(choices) < 2:
                    # Fallback to meaningful choices if AI didn't provide good ones
                    choices = [
                        "Continue forward",
                        "Look around carefully", 
                        "Pause and consider options"
                    ]
                    print("[DEBUG] Using fallback choices - AI response invalid")
                
                self.renderer.show_choices(choices, intensity)
                
                # Get player input (with secret word detection)
                def secret_check(input_text):
                    return self.truth.process_secret_input(
                        input_text,
                        context['hidden_stats']['sanity'],
                        context['choice_count']
                    )
                
                choice_idx = self.renderer.get_choice_input(len(choices), secret_check)
                chosen_text = choices[choice_idx]
                
                # Check for choice patterns
                pattern_response = self.truth.detect_choice_pattern(choice_idx + 1)
                if pattern_response:
                    self.renderer.console.print(f"\n[dim italic yellow]{pattern_response}[/]")
                    time.sleep(1.5)
                
                # Occasionally lie about what they chose (meta trick)
                if random.random() < 0.05 and context['choice_count'] > 5:
                    # Show them they "chose" something different
                    fake_idx = random.choice([i for i in range(len(choices)) if i != choice_idx])
                    self.renderer.console.print(f"\n[dim italic]Wait... did you choose option {fake_idx + 1}? I could have sworn...[/]")
                    time.sleep(1.0)
                    self.renderer.console.print("[dim italic]No, no, you're right. Option {choice_idx + 1}. Definitely.[/]\n")
                    time.sleep(0.8)
                
                # Process choice
                self.story.process_choice(chosen_text, choice_idx)
                
                # Generate next scene with revelation context
                self.renderer.show_loading(self.typography.get_loading_glitch(), 1.0)
                
                # Add revelation modifiers to context
                current_context = self.story.get_context()
                current_context['revelation_level'] = self.truth.revelation_level
                revelation_mods = get_revelation_modifiers(self.truth.revelation_level, breadcrumb_active)
                current_context['revelation_context'] = revelation_mods
                
                next_scene = self.ai.generate_scene(current_context)
                
                if next_scene.get('error'):
                    self.renderer.show_error_glitch(next_scene['narrative'])
                
                # Update narrative for next iteration  
                self.story.set_narrative(next_scene.get('narrative', ''))
                
                # Store for next loop - this is what we'll display
                opening = next_scene
                
                # Debug: Check if we got valid data
                if not next_scene.get('choices') or len(next_scene.get('choices', [])) < 2:
                    print(f"[DEBUG] Next scene has invalid choices: {next_scene.get('choices')}")
                    print(f"[DEBUG] Next scene narrative length: {len(next_scene.get('narrative', ''))}")
                
                # Occasional special visual moments
                if intensity > 0.7 and random.choice([True, False, False]):
                    self._trigger_special_moment(context)
            
            # Save ghost memory on exit (with truth state)
            self.session.save_ghost_memory(
                self.story.choice_history,
                self.story.get_state_summary(),
                self.truth.get_state_dict()
            )
            
            self.renderer.console.print("\n[dim]Session saved to ghost memory.[/]")
            self.renderer.console.print("[dim]You can run this again. It will be different.[/]")
            self.renderer.console.print("[dim](it always is)[/]\n")
        
        except KeyboardInterrupt:
            self.renderer.console.print("\n\n[dim]Interrupted. The story fragments disperse.[/]")
            # Still save ghost memory
            self.session.save_ghost_memory(
                self.story.choice_history,
                self.story.get_state_summary(),
                self.truth.get_state_dict()
            )
            sys.exit(0)
        
        except Exception as e:
            self.renderer.console.print(f"\n\n[bold red]CRITICAL ERROR:[/] {str(e)}")
            self.renderer.console.print("[dim]The narrator has stopped responding.[/]")
            sys.exit(1)
    
    def _trigger_special_moment(self, context: Dict):
        """Trigger special typographic moments."""
        import random
        
        moment_types = ['mirror', 'falling', 'emphasis', 'whisper']
        moment = random.choice(moment_types)
        
        texts = [
            "you are being watched",
            "this isn't real",
            "turn back",
            "the walls remember",
            "who are you?"
        ]
        
        self.renderer.show_special_moment(moment, random.choice(texts))


def main():
    """Entry point - the story begins immediately."""
    game = Game()
    game.run()


if __name__ == "__main__":
    # No menu. No introduction. Just begin.
    main()

