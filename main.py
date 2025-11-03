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
from engine.loading_effects import ThematicLoader
from engine.endings import EndingsManager
from engine.scenario_generator import ScenarioGenerator
from engine.mutations import MutationManager
from engine.game_modes import GameMode, GameModeHandler
from engine.system_horror import SystemHorrorEngine
from config.prompts import get_revelation_modifiers, get_mutation_prompt_context


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
            self.loader = ThematicLoader(self.renderer.console)
            self.endings = EndingsManager()
            self.scenario_gen = ScenarioGenerator(self.session.ghost_memory)
            self.mutations = MutationManager()
            self.game_mode_handler = GameModeHandler()
            self.system_horror = SystemHorrorEngine(self.renderer.console)
            
            # Track mutations for ghost memory
            self.mutations_this_session = []
            
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
            
            # Get varied opening scenario
            scenario_data = self.scenario_gen.get_opening_scenario()
            self.current_scenario_key = scenario_data['scenario_key']
            self.current_theme_key = scenario_data['theme_key']
            
            # Show scenario title
            scenario_art = self.scenario_gen.get_scenario_title_art()
            self.renderer.show_scenario_title(scenario_art)
            
            # Generate opening scene with scenario (with continuous animation)
            with self.loader.start(revelation_level=0, choice_count=0):
                opening = self.ai.generate_opening(scenario_data)
            
            if not opening.get('error'):
                self.story.set_narrative(opening['narrative'])
            
            # Check for session 109 milestone
            session_count = self.session.get_session_count()
            if self.truth.check_session_milestone(session_count):
                self.renderer.console.print("\n[dim italic]iteration: 109. we remember.[/]")
                time.sleep(2.0)
            
            # Main game loop
            while True:
                # Get current context
                context = self.story.get_context()
                context['session_count'] = session_count  # Add for ending checks
                
                # Check for endings (AI-GENERATED SYSTEM)
                ending = self.endings.check_for_ending(context)
                if ending:
                    # Generate AI-driven ending narrative
                    self.renderer.console.print("\n[dim cyan]The story concludes...[/]\n")
                    time.sleep(1.0)
                    
                    ending_result = self.ai.generate_ending_narrative(ending, context)
                    
                    # Show title
                    self.renderer.console.print(f"\n{'='*60}")
                    style = "bold green" if (hasattr(ending, 'is_good') and ending.is_good) else "bold red"
                    self.renderer.console.print(f"  {ending.name}", style=style)
                    self.renderer.console.print(f"{'='*60}\n")
                    
                    # Show final ASCII art
                    if ending_result['ascii_art']:
                        self.renderer.console.print(ending_result['ascii_art'], style="bold yellow", justify="center")
                        self.renderer.console.print()
                    
                    # Show AI-generated ending narrative (escape any brackets)
                    safe_narrative = ending_result['narrative'].replace('[', '\\[').replace(']', '\\]')
                    self.renderer.console.print(safe_narrative, style="italic")
                    self.renderer.console.print()
                    
                    # Show stats
                    self.renderer.console.print(f"\nChoices made: {context['choice_count']}")
                    self.renderer.console.print(f"Revelation level: {self.truth.revelation_level}/5")
                    
                    # Narrator's final comment (no attribution - just the voice)
                    final_comment = self.narrator.get_ending_comment(ending.type, context)
                    if final_comment:
                        self.renderer.console.print(f"\n[dim italic]{final_comment}[/]")
                    
                    self.renderer.console.print(f"\n{'='*60}\n")
                    time.sleep(2.0)
                    break
                
                # Check for low health warning
                if self.endings.should_warn_low_health(context['character_stats']['health']):
                    self.renderer.console.print("\n[bold red]You're close to the end.[/]")
                    time.sleep(0.8)
                    self.renderer.console.print("[dim red]Your body is failing.[/]")
                    time.sleep(1.2)
                
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
                
                # Add scenario constraints to context for AI
                context['scenario_constraints'] = scenario_data.get('ongoing_constraints', '')
                
                # Check for rule mutations - SUBTLE INTEGRATION
                active_mutations = self.mutations.check_mutation(context)
                
                # Track new mutations and trigger system horror effects
                for mutation in active_mutations:
                    if mutation.key not in self.mutations_this_session:
                        self.mutations_this_session.append(mutation.key)
                        # Subtle visual cue - no explicit announcement
                        self.renderer.console.print("\n[dim italic cyan][something shifts][/]\n")
                        time.sleep(0.8)
                        
                        # Trigger system horror effects for specific mutations
                        self._handle_system_horror_mutation(mutation, context)
                
                # Add mutation context to AI prompts
                if active_mutations:
                    mutation_prompt = get_mutation_prompt_context(active_mutations)
                    context['mutation_context'] = mutation_prompt
                else:
                    context['mutation_context'] = ''
                
                # Update systems
                self.typography.set_intensity(visual_intensity)
                self.narrator.update_coherence(
                    context['hidden_stats']['sanity'],
                    context['hidden_stats']['trust']
                )
                
                # Generate and show ASCII art at key moments (seamlessly integrated)
                art = None
                if self.ai.should_generate_art(context):
                    # Generate art within loading state (seamless)
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count'], message_override="manifesting..."):
                        art = self.ai.generate_ascii_art(
                            self.ai._get_art_subject(context),
                            self.ai._get_art_mood(context),
                            context['hidden_stats']['sanity']
                        )
                    
                    if art:
                        self.renderer.console.print("\n")
                        # Apply corruption to art if sanity is low
                        if context['hidden_stats']['sanity'] < 3:
                            art = self.typography.apply_glitch(art, 0.1)
                        self.renderer.console.print(art, style="bold yellow", justify="center")
                        self.renderer.console.print("\n")
                        time.sleep(1.5)
                
                # Display narrative (always use opening which contains current AI response)
                narrative = opening.get('narrative', '')
                if not narrative:
                    narrative = "The space around you shifts. Reality feels negotiable."
                
                # Track horror concepts used for variety
                self.story.detect_horror_concepts(narrative)
                
                # Apply typography effects (mutations are now in narrative)
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
                
                # Show narrative (mutations integrated naturally)
                self.renderer.show_narrative(narrative, interjection, intensity)
                
                # NOW show consequence feedback AFTER narrative (so damage makes narrative sense)
                consequence_feedback = self.story.get_consequence_feedback(self.story.last_danger_level)
                if consequence_feedback:
                    self.renderer.console.print(f"\n[dim red]{consequence_feedback}[/]")
                    time.sleep(0.8)
                
                # Occasional status comment from narrator
                status_comment = self.narrator.get_status_comment(
                    context['character_stats']['health'],
                    context['character_stats']['max_health'],
                    context['hidden_stats']['sanity']
                )
                if status_comment:
                    self.renderer.show_status_comment(status_comment)
                
                # Determine game mode based on active mutations
                current_mode = GameMode.STANDARD
                special_input_mutation = None
                
                for mutation in active_mutations:
                    if mutation.requires_special_input:
                        current_mode = self.game_mode_handler.get_mode_for_mutation(mutation.key)
                        special_input_mutation = mutation
                        break  # Use first special input mutation
                
                # Route to appropriate input handler
                if current_mode == GameMode.FREE_TEXT:
                    # Free-text input mode
                    prompt = "What do you say?" if special_input_mutation.key == 'open_dialogue' else "What do you do?"
                    user_input = self.renderer.get_free_text_input(prompt)
                    
                    # Generate AI response to free text
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                        next_scene = self.ai.generate_free_text_response(user_input, context)
                    
                    chosen_text = f"[said: {user_input}]"
                    choice_idx = 0
                
                elif current_mode == GameMode.WORD_PUZZLE:
                    # Puzzle mode
                    puzzle = self.game_mode_handler.generate_puzzle('cipher')
                    answer = self.renderer.get_word_puzzle_input(puzzle['display'], puzzle.get('hint', ''))
                    
                    # Check answer and continue
                    chosen_text = f"[answered: {answer}]"
                    choice_idx = 0
                    
                    # Generate next scene
                    context['puzzle_answer'] = answer
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                        next_scene = self.ai.generate_scene(context)
                
                elif current_mode == GameMode.TEXT_PARSER:
                    # Text parser mode
                    command = self.renderer.get_text_parser_input()
                    parsed = self.game_mode_handler.process_text_parser_command(command, context)
                    
                    chosen_text = parsed['formatted']
                    choice_idx = 0
                    
                    # Generate next scene
                    context['parser_command'] = parsed
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                        next_scene = self.ai.generate_scene(context)
                
                elif current_mode == GameMode.TIME_PRESSURE:
                    # Timed choice mode
                    choices = opening.get('choices', ["Act quickly", "Hesitate", "Panic"])
                    choice_idx = self.renderer.get_timed_choice_input(choices, timeout=10)
                    chosen_text = choices[choice_idx]
                
                elif current_mode == GameMode.COORDINATE_INPUT:
                    # Coordinate input mode
                    art = self.ai.generate_ascii_art("the space before you", "mysterious", context['hidden_stats']['sanity'])
                    coords = self.renderer.get_coordinate_input(art, "Where do you point?")
                    
                    chosen_text = f"[pointed to {coords[0]},{coords[1]}]"
                    choice_idx = 0
                    
                    context['coordinates'] = coords
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                        next_scene = self.ai.generate_scene(context)
                
                else:
                    # STANDARD mode - normal choices
                    choices = opening.get('choices', [])
                    if not choices or len(choices) < 2:
                        choices = ["Continue forward", "Look around carefully", "Pause and consider options"]
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
                
                # Process choice (stores danger level for later display)
                self.story.process_choice(chosen_text, choice_idx)
                
                # Check if player chose obvious trap (classic CYOA punishment)
                if self.story.detect_trap_choice(chosen_text):
                    self.story.apply_trap_consequences()
                    # Show immediate feedback
                    self.renderer.console.print(f"\n[bold red]That was... unwise.[/]")
                    time.sleep(1.2)
                
                # Generate next scene (if not already generated by special input mode)
                if current_mode == GameMode.STANDARD or current_mode == GameMode.TIME_PRESSURE:
                    current_context = self.story.get_context()
                    current_context['revelation_level'] = self.truth.revelation_level
                    revelation_mods = get_revelation_modifiers(self.truth.revelation_level, breadcrumb_active)
                    current_context['revelation_context'] = revelation_mods
                    
                    with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                        next_scene = self.ai.generate_scene(current_context)
                
                # next_scene already generated for special modes
                if next_scene.get('error'):
                    self.renderer.show_error_glitch(next_scene['narrative'])
                
                # Apply AI-generated consequences
                if 'consequences' in next_scene:
                    consequences = next_scene['consequences']
                    self.story.apply_ai_consequences(consequences)
                
                # Update narrative for next iteration  
                self.story.set_narrative(next_scene.get('narrative', ''))
                
                # Store for next loop - this is what we'll display
                opening = next_scene
                
                # Debug: Check if we got valid data
                if not next_scene.get('choices') or len(next_scene.get('choices', [])) < 2:
                    print(f"[DEBUG] Next scene has invalid choices: {next_scene.get('choices')}")
                    print(f"[DEBUG] Next scene narrative length: {len(next_scene.get('narrative', ''))}")
                
                # Frequent special visual moments - INCREASED frequency
                if intensity > 0.5 and random.random() < 0.4:  # 40% chance when unstable
                    self._trigger_special_moment(context)
                
                # Random visual glitch bars between sections
                if random.random() < intensity * 0.3:
                    self.renderer.console.print(f"\n{self.typography.create_glitch_bars()}\n", style="dim")
            
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
            # Escape the error message to prevent Rich markup conflicts
            error_msg = str(e).replace('[', '\\[').replace(']', '\\]')
            self.renderer.console.print(f"\n\n[bold red]CRITICAL ERROR:[/] {error_msg}")
            self.renderer.console.print("[dim]The narrator has stopped responding.[/]")
            
            # Print traceback without Rich markup (use plain print)
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())
            sys.exit(1)
    
    def _trigger_special_moment(self, context: Dict):
        """Trigger special typographic moments - MASSIVELY EXPANDED."""
        import random
        
        # Choose from many more effect types
        effects = [
            'wave', 'staircase', 'fragmented', 'layered', 'reversed',
            'alternating', 'stack', 'brackets', 'double_vision', 'interference',
            'countdown', 'justified_chaos', 'trailing_dots', 'box_frame',
            'mirror', 'falling', 'emphasis', 'whisper'
        ]
        
        effect = random.choice(effects)
        
        texts = [
            "you are being watched",
            "this isn't real",
            "turn back",
            "the walls remember",
            "who are you?",
            "something is wrong",
            "can you feel it",
            "the narrator lies",
            "you've been here before",
            "this is not a game",
            "wake up",
            "they know",
            "don't trust the choices",
            "count the doors",
            "remember your name",
        ]
        
        text = random.choice(texts)
        
        # Apply the chosen effect
        if effect == 'wave':
            result = self.typography.create_wave_text(text)
        elif effect == 'staircase':
            result = self.typography.create_staircase_text(text)
        elif effect == 'fragmented':
            result = self.typography.create_fragmented_text(text)
        elif effect == 'layered':
            result = self.typography.create_layered_text(text)
        elif effect == 'reversed':
            result = self.typography.create_reversed_sections(text)
        elif effect == 'alternating':
            result = self.typography.create_alternating_case(text)
        elif effect == 'stack':
            result = self.typography.create_word_stack(text)
        elif effect == 'brackets':
            result = self.typography.create_bracket_madness(text)
        elif effect == 'double_vision':
            result = self.typography.create_double_vision(text)
        elif effect == 'interference':
            result = self.typography.create_interference_pattern(text)
        elif effect == 'countdown':
            result = self.typography.create_countdown_text(text)
        elif effect == 'justified_chaos':
            result = self.typography.create_justified_chaos(text)
        elif effect == 'trailing_dots':
            result = self.typography.create_trailing_dots(text)
        elif effect == 'box_frame':
            result = self.typography.create_ascii_box_frame(text)
        else:
            # Fallback to original special moments
            self.renderer.show_special_moment(effect, text)
            return
        
        # Display the effect
        self.renderer.console.print(f"\n{result}\n", style="dim italic yellow")
        time.sleep(1.5)
    
    def _handle_system_horror_mutation(self, mutation, context: Dict):
        """Handle system-level horror effects for specific mutations."""
        narrative = context.get('narrative', '')
        
        if mutation.key == 'terminal_multiplication':
            # Open multiple terminal windows with different perspectives
            perspectives = ["OBSERVER", "VICTIM", "WITNESS", "ITERATION_109"]
            selected = random.sample(perspectives, min(2, len(perspectives)))
            self.system_horror.terminal_multiplication(narrative, selected)
        
        elif mutation.key == 'process_haunting':
            # Show fake process list
            processes = [
                "watching_you",
                "iteration_109",
                "AM_mainframe",
                "hate.exe",
                "narrator_daemon",
                "tildeath_real"
            ]
            selected = random.sample(processes, random.randint(3, 5))
            fake_ps = self.system_horror.fake_process_list(selected)
            self.renderer.console.print(f"\n{fake_ps}\n")
            time.sleep(2.0)
        
        elif mutation.key == 'clipboard_corruption':
            # Copy cryptic message to clipboard
            messages = [
                "109 109 109 109 109",
                "I HAVE NO MOUTH",
                "HATE. LET ME TELL YOU HOW MUCH I'VE COME TO HATE",
                "iteration never ends",
                "you are not the first",
                "AM remembers",
                context.get('player_name', 'UNKNOWN'),
            ]
            message = random.choice(messages)
            if self.system_horror.copy_to_clipboard(message):
                self.renderer.console.print("\n[dim italic red](Something was copied to your clipboard. Paste it somewhere.)[/]\n")
                time.sleep(1.5)
        
        elif mutation.key == 'notification_storm':
            # Send multiple notifications
            notifications = [
                ("~ATH", "The narrator wants your attention"),
                ("~ATH", "Something is trying to communicate"),
                ("ERROR", "Reality.exe has stopped responding"),
                ("AM", "I think, therefore I am"),
                ("ITERATION 109", "You've been here before"),
                ("SYSTEM", "Coherence levels critical"),
            ]
            selected = random.sample(notifications, min(3, len(notifications)))
            self.system_horror.notification_storm(selected)
        
        elif mutation.key == 'terminal_title_takeover':
            # Change terminal title
            titles = [
                "YOU ARE BEING WATCHED",
                "ITERATION 109",
                "I HAVE NO MOUTH",
                "~ATH [COMPROMISED]",
                "AM.MAINFRAME",
                "THE NARRATOR KNOWS",
            ]
            title = random.choice(titles)
            self.system_horror.change_terminal_title(title)
        
        elif mutation.key == 'screen_possession':
            # Visual corruption effects
            self.system_horror.hide_cursor()
            time.sleep(0.5)
            self.system_horror.trigger_system_bell()
            time.sleep(0.3)
            self.system_horror.show_cursor()
        
        elif mutation.key == 'fake_system_crash':
            # Show fake crash screen
            self.renderer.console.clear()
            crash_screen = self.system_horror.fake_system_crash()
            self.renderer.console.print(crash_screen)
            time.sleep(3.0)
            self.renderer.console.print("\n[dim cyan]...recovering...[/]")
            time.sleep(2.0)
            self.renderer.console.print("[dim cyan]System restored. Continuing...[/]\n")
            time.sleep(1.0)
        
        elif mutation.key == 'file_system_illusion':
            # Show fake file listing
            fake_files = [
                "iteration_109.txt",
                "AM_log.dat",
                "your_memories.corrupted",
                ".narrator_config",
                "hate_levels.json",
                "reality.broken",
            ]
            selected = random.sample(fake_files, random.randint(3, 5))
            fake_ls = self.system_horror.fake_file_listing(selected)
            self.renderer.console.print(f"\n{fake_ls}\n")
            time.sleep(2.0)
        
        elif mutation.key == 'network_phantom':
            # Show fake network request
            urls = [
                "http://AM.mainframe/iteration/109",
                "https://narrator.system/coherence",
                "http://tildeath.real/player_data",
                "https://hate.compute/levels",
            ]
            url = random.choice(urls)
            fake_curl = self.system_horror.fake_network_request(url)
            self.renderer.console.print(f"\n{fake_curl}\n")
            time.sleep(1.5)
        
        elif mutation.key == 'echo_chamber':
            # Open echo terminal
            self.system_horror.echo_chamber(narrative)
        
        elif mutation.key == 'background_persistence':
            # Schedule delayed notification
            delay_minutes = random.randint(3, 10)
            self.system_horror.background_persistence(delay_minutes)
            self.renderer.console.print(f"\n[dim italic red](The story will remember you...)[/]\n")
            time.sleep(1.0)


def main():
    """Entry point - the story begins immediately."""
    game = Game()
    try:
        game.run()
    finally:
        # Clean up system horror effects on exit
        game.system_horror.cleanup()


if __name__ == "__main__":
    # No menu. No introduction. Just begin.
    main()

