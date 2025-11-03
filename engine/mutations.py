"""Reality-bending rule mutation system - COMPLETELY OVERHAULED."""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class MutationType(Enum):
    """Category of mutation."""
    MODERATE = "moderate"  # Early-mid game
    WILD = "wild"  # High revelation, late game


class MutationState(Enum):
    """Lifecycle state of a mutation."""
    ACTIVATING = "activating"  # First turn, being introduced
    ACTIVE = "active"  # Fully active
    STACKING = "stacking"  # Active with other mutations
    FADING = "fading"  # Last turn, ending


class MutationRarity(Enum):
    """Rarity tier for mutations."""
    COMMON = "common"  # 60% - Visual effects, choice mods
    UNCOMMON = "uncommon"  # 30% - Format shifts, narrator changes
    RARE = "rare"  # 8% - Genre shifts, free-text modes
    ULTRA_RARE = "ultra_rare"  # 2% - Complete transformations


@dataclass
class Mutation:
    """A rule-breaking gameplay mutation."""
    name: str
    key: str
    type: MutationType
    rarity: MutationRarity
    description: str
    narrative_trigger: str  # How AI introduces it in story
    discovery_method: str  # How player realizes it's active
    duration: int  # How many turns it lasts (0 = one-shot effect)
    can_stack: bool  # Can be active with other mutations
    fade_narrative: str  # How it ends in story
    requires_special_input: bool = False  # Needs non-standard input
    
    def __eq__(self, other):
        if isinstance(other, Mutation):
            return self.key == other.key
        return self.key == other


class MutationManager:
    """Manages selection and application of rule mutations."""
    
    # MODERATE MUTATIONS (Common/Uncommon - Visual & Choice mods)
    MODERATE_MUTATIONS = [
        # COMMON (60% of moderate)
        Mutation(
            "Choice Inflation",
            "choice_inflation",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Suddenly provides 6-8 choices instead of normal 3-4",
            "The possibilities multiply before you, branching into too many paths",
            "Player sees 6-8 choices instead of usual 3-4",
            1,
            True,
            "The excess options fade away, leaving only the essential",
            False
        ),
        Mutation(
            "Choice Drought",
            "choice_drought",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Only 2 choices, both clearly bad",
            "Your options narrow. The walls close in",
            "Player sees only 2 choices, both ominous",
            1,
            True,
            "More possibilities return, though you're not sure if that's better",
            False
        ),
        Mutation(
            "Hidden Choice",
            "hidden_choice",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "One choice is blank/corrupted, mystery option",
            "One of the paths ahead is obscured, unreadable",
            "One choice appears as ░░░░░░░░",
            1,
            True,
            "The obscured path becomes clear again",
            False
        ),
        Mutation(
            "Reverse Choices",
            "reverse_choices",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Choices listed backwards",
            "Everything inverts. Up becomes down. First becomes last",
            "Choices appear in reverse order",
            1,
            True,
            "Order reasserts itself",
            False
        ),
        Mutation(
            "Duplicate Choices",
            "duplicate_choices",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Same choice appears 3 times with tiny variations",
            "The same path repeats, slightly different each time",
            "Same choice appears multiple times",
            1,
            True,
            "The duplicates collapse into one",
            False
        ),
        Mutation(
            "Margin Madness",
            "margin_madness",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Marginalia and notes appear in the text",
            "Notes appear in the margins. Whose handwriting is that?",
            "Text has marginal notes and annotations",
            2,
            True,
            "The margins clear themselves",
            False
        ),
        Mutation(
            "Redaction Protocol",
            "redaction",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Parts of narrative are censored/blacked out",
            "Someone is censoring the story. Black bars cover the truth",
            "Parts of text are ██████ blacked out",
            1,
            True,
            "The redactions lift",
            False
        ),
        Mutation(
            "Echo Chamber Active",
            "echo_active",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Words repeat and echo across screen",
            "Words echo echo echo through the space",
            "Key words repeat multiple times",
            1,
            True,
            "The echoes fade to silence",
            False
        ),
        Mutation(
            "Diagonal Slide",
            "diagonal_slide",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Text slides diagonally down screen",
            "Gravity shifts. Everything slides sideways",
            "Text appears diagonally",
            1,
            True,
            "Gravity normalizes",
            False
        ),
        Mutation(
            "Scattered Thoughts",
            "scattered",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Words scattered randomly across screen",
            "Your thoughts scatter. Coherence fragments",
            "Words appear scattered across screen",
            1,
            True,
            "Thoughts coalesce again",
            False
        ),
        Mutation(
            "Breathing Text",
            "breathing_text",
            MutationType.MODERATE,
            MutationRarity.COMMON,
            "Spacing expands and contracts",
            "The text breathes. In. Out. In. Out",
            "Spacing between words pulses",
            2,
            True,
            "The breathing stops",
            False
        ),
        
        # UNCOMMON (30% of moderate)
        Mutation(
            "No Narrative",
            "no_narrative",
            MutationType.MODERATE,
            MutationRarity.UNCOMMON,
            "Just choices, no story text this turn",
            "The story goes silent. Only choices remain",
            "No narrative text, only choices",
            1,
            False,
            "The narrator finds their voice again",
            False
        ),
        Mutation(
            "No Choices",
            "no_choices",
            MutationType.MODERATE,
            MutationRarity.UNCOMMON,
            "Just narrative, auto-continues after pause",
            "You have no say in what happens next",
            "No choices appear, story continues automatically",
            1,
            False,
            "Your agency returns",
            False
        ),
        Mutation(
            "Stat Reveal",
            "stat_reveal",
            MutationType.MODERATE,
            MutationRarity.UNCOMMON,
            "Suddenly shows hidden stats, then hides again",
            "For a moment, you see the numbers behind everything",
            "Hidden stats briefly visible",
            0,
            True,
            "The numbers vanish again",
            False
        ),
        Mutation(
            "Box Collapse",
            "box_collapse",
            MutationType.MODERATE,
            MutationRarity.UNCOMMON,
            "Text trapped in shrinking boxes",
            "The words are trapped, boxed in, compressed",
            "Text appears in nested boxes",
            1,
            True,
            "The boxes open",
            False
        ),
    ]
    
    # WILD MUTATIONS (Uncommon/Rare/Ultra-rare - Format shifts & Genre changes)
    WILD_MUTATIONS = [
        # UNCOMMON WILD (30%)
        Mutation(
            "Narrator Split",
            "narrator_split",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Two narrators arguing about what happens",
            "Two voices speak at once, contradicting each other",
            "Two columns of text, both claiming truth",
            2,
            True,
            "One voice falls silent. The other continues alone",
            False
        ),
        Mutation(
            "Format Shift",
            "format_shift",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Game becomes poetry, chat log, error messages, etc.",
            "The format corrupts. This isn't a story anymore",
            "Text appears as poetry/code/chat log",
            2,
            True,
            "Format stabilizes back to prose",
            False
        ),
        Mutation(
            "Fourth Wall Breach",
            "fourth_wall",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Narrator addresses player directly about their terminal/life",
            "The narrator looks directly at you. Through the screen",
            "Narrator mentions your terminal, your room, you",
            1,
            True,
            "The narrator looks away",
            False
        ),
        Mutation(
            "Format Corruption",
            "format_corruption",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Output becomes pure ASCII art, code, or glitch",
            "Everything corrupts into static and symbols",
            "Heavy glitch effects on all text",
            1,
            True,
            "Signal clears",
            False
        ),
        Mutation(
            "Static Vision",
            "static_vision",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Heavy static overlays all text",
            "Static fills your vision. You can barely read through it",
            "Text obscured by █▓▒░ static",
            1,
            True,
            "Static clears",
            False
        ),
        Mutation(
            "Mirror Reality",
            "mirror_reality",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Text and its reverse displayed simultaneously",
            "You see the story and its reflection at once",
            "Text appears with reversed mirror below",
            1,
            True,
            "The mirror shatters",
            False
        ),
        Mutation(
            "Fade to Nothing",
            "fade_nothing",
            MutationType.WILD,
            MutationRarity.UNCOMMON,
            "Text progressively fades away",
            "Everything is fading. Disappearing. Going dark",
            "Text becomes progressively dimmer",
            1,
            True,
            "Color returns",
            False
        ),
        
        # RARE WILD (8%) - Genre shifts and special inputs
        Mutation(
            "Open Dialogue",
            "open_dialogue",
            MutationType.WILD,
            MutationRarity.RARE,
            "Talk freely with narrator/entities",
            "A voice asks: 'What do you want to say?'",
            "Free text input instead of choices",
            3,
            False,
            "The conversation ends. Choices return",
            True
        ),
        Mutation(
            "Confession Booth",
            "confession_booth",
            MutationType.WILD,
            MutationRarity.RARE,
            "Narrator asks personal questions",
            "The narrator wants to know about you. The real you",
            "Personal questions requiring free text",
            2,
            False,
            "The interrogation ends",
            True
        ),
        Mutation(
            "Reality Argument",
            "reality_argument",
            MutationType.WILD,
            MutationRarity.RARE,
            "Debate what's real via text input",
            "The narrator challenges you: 'Prove this is real'",
            "Debate with narrator via free text",
            3,
            False,
            "The argument reaches no conclusion",
            True
        ),
        Mutation(
            "Name the Horror",
            "name_horror",
            MutationType.WILD,
            MutationRarity.RARE,
            "Describe what you see in your own words",
            "The narrator can't describe it. You must",
            "Must describe scene in own words",
            2,
            False,
            "The narrator takes over again",
            True
        ),
        Mutation(
            "Time Pressure",
            "time_pressure",
            MutationType.WILD,
            MutationRarity.RARE,
            "10-second timer added to input",
            "Time accelerates. You must choose NOW",
            "10-second countdown appears",
            1,
            False,
            "Time returns to normal",
            True
        ),
        Mutation(
            "Cipher Lock",
            "cipher_lock",
            MutationType.WILD,
            MutationRarity.RARE,
            "Decode message to continue",
            "The path forward is encrypted. Decode it",
            "Puzzle must be solved",
            2,
            False,
            "The cipher unlocks",
            True
        ),
        Mutation(
            "Word Association",
            "word_association",
            MutationType.WILD,
            MutationRarity.RARE,
            "Rapid-fire word game",
            "Complete the pattern. Quickly",
            "Word puzzle appears",
            1,
            False,
            "The game ends",
            True
        ),
        Mutation(
            "Memory Test",
            "memory_test",
            MutationType.WILD,
            MutationRarity.RARE,
            "Recall previous events",
            "The narrator tests your memory of what came before",
            "Questions about previous choices",
            1,
            False,
            "The test concludes",
            True
        ),
        Mutation(
            "Text Parser",
            "text_parser",
            MutationType.WILD,
            MutationRarity.RARE,
            "Old-school LOOK/TAKE/GO commands",
            "The interface shifts. Type commands like LOOK AROUND",
            "Must use verb-noun commands",
            3,
            False,
            "Modern choices return",
            True
        ),
        Mutation(
            "Coordinate Input",
            "coordinate_input",
            MutationType.WILD,
            MutationRarity.RARE,
            "Navigate ASCII art by coordinates",
            "An image appears. Point to where you want to go",
            "ASCII art with coordinate input",
            2,
            False,
            "The image fades",
            True
        ),
        Mutation(
            "Reverse Narration",
            "reverse_narration",
            MutationType.WILD,
            MutationRarity.RARE,
            "Player becomes narrator",
            "The narrator falls silent. It's your turn to tell the story",
            "Must type what happens next",
            2,
            False,
            "The narrator reclaims their role",
            True
        ),
        Mutation(
            "Fill the Blanks",
            "fill_blank",
            MutationType.WILD,
            MutationRarity.RARE,
            "Narrative has gaps to fill",
            "The story has holes. You _____ fill them",
            "Narrative with _____ blanks",
            2,
            False,
            "The story becomes whole again",
            True
        ),
        
        # ULTRA-RARE WILD (2%) - Complete transformations
        Mutation(
            "Debug Mode",
            "debug_mode",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Fake debug console with story variables",
            "DEBUG MODE ACTIVATED. You see the code behind the story",
            "Debug console with fake variables",
            4,
            False,
            "DEBUG MODE TERMINATED",
            True
        ),
        Mutation(
            "Code Editor",
            "code_editor",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "'Edit' the story's source code",
            "You're looking at the source code. Can you change it?",
            "Fake code editor interface",
            4,
            False,
            "Editor closes. Changes may or may not persist",
            True
        ),
        Mutation(
            "Temporal Loop",
            "temporal_loop",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Next 3 choices repeat your last 3 exactly",
            "Time loops. You've done this before. You'll do it again",
            "Choices repeat previous ones",
            3,
            False,
            "The loop breaks",
            False
        ),
        Mutation(
            "Cross-Session Bleed",
            "cross_session",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "References to 'other iterations' appear",
            "You remember other versions of this. Other yous",
            "References to previous playthroughs",
            2,
            True,
            "The memories fade",
            False
        ),
        Mutation(
            "Computer Horror",
            "computer_horror",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Meta messages about your actual computer/terminal",
            "The story knows things about your computer it shouldn't",
            "References to your actual system",
            1,
            True,
            "The story looks away from your machine",
            False
        ),
        Mutation(
            "Terminal Takeover",
            "terminal_takeover",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Fake terminal commands interrupt story",
            "Your terminal is compromised. Commands appear unbidden",
            "Fake shell commands in narrative",
            2,
            True,
            "You regain control",
            False
        ),
        Mutation(
            "Spiral Narrative",
            "spiral_narrative",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Text spirals across the screen",
            "Everything spirals. Down. Down. Down",
            "Text in spiral pattern",
            1,
            True,
            "The spiral straightens",
            False
        ),
        Mutation(
            "ASCII Intrusion",
            "ascii_intrusion",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Creepy ASCII art interrupts narrative",
            "An image forces itself into your vision",
            "Large ASCII art interrupts text",
            0,
            True,
            "The image fades",
            False
        ),
        Mutation(
            "Permission Error",
            "permission_error",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Fake permission denied messages",
            "ACCESS DENIED. You don't have permission to continue",
            "Fake system error messages",
            0,
            True,
            "Access granted",
            False
        ),
        Mutation(
            "Memory Rewrite",
            "memory_rewrite",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Previous choice gets retconned",
            "Wait. That's not what happened. The past changes",
            "Narrator contradicts previous events",
            0,
            True,
            "History settles into one version",
            False
        ),
        Mutation(
            "Choice Rebellion",
            "choice_rebellion",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Your selection gets overridden mid-action",
            "You choose one thing. Something else happens instead",
            "Choice overridden by narrator",
            0,
            True,
            "Your will reasserts itself",
            False
        ),
        Mutation(
            "Forced Random",
            "forced_random",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Narrator auto-selects a choice for you",
            "The narrator makes the choice for you",
            "Choice made automatically",
            0,
            True,
            "You regain control",
            False
        ),
        
        # ====================================================================
        # SYSTEM HORROR MUTATIONS - Ultra-rare system-level effects
        # ====================================================================
        
        Mutation(
            "Terminal Multiplication",
            "terminal_multiplication",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "The terminal splits. You see yourself from multiple angles",
            "Reality fractures. Multiple perspectives emerge",
            "Multiple terminal windows open",
            3,
            False,
            "The extra windows close themselves",
            True
        ),
        Mutation(
            "Process Haunting",
            "process_haunting",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Game appears in process list with disturbing names",
            "Check your running processes. Something's wrong",
            "Fake process list with story processes",
            4,
            True,
            "The processes normalize",
            False
        ),
        Mutation(
            "Clipboard Corruption",
            "clipboard_corruption",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Copies cryptic messages to clipboard without warning",
            "Your fingers move without thinking. Something copies itself",
            "Text copied to system clipboard",
            2,
            True,
            "Your clipboard returns to normal",
            False
        ),
        Mutation(
            "Notification Storm",
            "notification_storm",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "OS notifications appear with story content",
            "Your computer wants to tell you something",
            "Multiple system notifications",
            1,
            False,
            "The notifications stop",
            False
        ),
        Mutation(
            "Terminal Title Takeover",
            "terminal_title_takeover",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Window title changes to reflect story state",
            "Look at your window title. It knows",
            "Terminal title changes dynamically",
            3,
            True,
            "The title returns to normal",
            False
        ),
        Mutation(
            "Screen Possession",
            "screen_possession",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Terminal appearance corrupts",
            "The screen itself begins to change",
            "Visual terminal corruption",
            2,
            False,
            "The screen stabilizes",
            False
        ),
        Mutation(
            "Fake System Crash",
            "fake_system_crash",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Displays fake kernel panic / BSOD",
            "Everything stops. The system fails",
            "Fake crash screen",
            0,
            False,
            "...recovering...",
            False
        ),
        Mutation(
            "File System Illusion",
            "file_system_illusion",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Pretends to create files in home directory",
            "Files appear that shouldn't exist",
            "Fake file listing",
            2,
            False,
            "The files were never real",
            False
        ),
        Mutation(
            "Network Phantom",
            "network_phantom",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Fake network requests to fictional servers",
            "Something is trying to connect",
            "Fake network activity",
            1,
            False,
            "Connection terminated",
            False
        ),
        Mutation(
            "Echo Chamber",
            "echo_chamber",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Opens second terminal that mirrors your choices",
            "You see yourself. Delayed. Watching",
            "Echo terminal opens",
            3,
            False,
            "The echo fades",
            False
        ),
        Mutation(
            "Background Persistence",
            "background_persistence",
            MutationType.WILD,
            MutationRarity.ULTRA_RARE,
            "Game schedules notifications after 'exit'",
            "The story will remember you",
            "Delayed notifications scheduled",
            0,
            False,
            "But will it let you go?",
            False
        ),
    ]
    
    def __init__(self):
        """Initialize mutation manager."""
        self.active_mutations: List[Tuple[Mutation, int, MutationState]] = []  # (mutation, turns_remaining, state)
        self.mutation_history: List[str] = []
        self.cooldown = 0
        self.combo_active: Optional[str] = None  # Active combo effect
    
    def check_mutation(self, context: Dict) -> List[Mutation]:
        """
        Check if mutations should occur this turn.
        Returns list of active mutations (can be multiple with stacking).
        """
        from engine.debug import debug_log
        
        choice_count = context.get('choice_count', 0)
        
        # DEBUG OUTPUT
        debug_log(f"\n[DEBUG MUTATION] Turn {choice_count}: Checking mutations...")
        debug_log(f"[DEBUG MUTATION] Active mutations: {len(self.active_mutations)}")
        debug_log(f"[DEBUG MUTATION] Cooldown: {self.cooldown}")
        
        # Update existing mutations
        self._update_active_mutations()
        
        # Decrement cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            debug_log(f"[DEBUG MUTATION] Cooldown decremented to {self.cooldown}")
        
        # GUARANTEED MUTATIONS - Import from settings
        from config.settings import MUTATION_GUARANTEED_AT
        
        debug_log(f"[DEBUG MUTATION] Guaranteed turns: {MUTATION_GUARANTEED_AT}")
        
        # Force mutation on guaranteed turns (even if cooldown active)
        if choice_count in MUTATION_GUARANTEED_AT:
            debug_log(f"[DEBUG MUTATION] GUARANTEED TURN! Forcing mutation...")
            new_mutation = self._try_trigger_mutation(context)
            if not new_mutation:  # If random failed, force one
                debug_log(f"[DEBUG MUTATION] Random failed, forcing mutation...")
                new_mutation = self._force_mutation(context)
            if new_mutation:
                debug_log(f"[DEBUG MUTATION] ✓ Activated: {new_mutation.name}")
                self._activate_mutation(new_mutation)
                # Don't set cooldown after guaranteed mutations!
                self.cooldown = 0
        elif self.cooldown == 0:
            # Normal mutation check
            debug_log(f"[DEBUG MUTATION] Cooldown at 0, trying random mutation...")
            new_mutation = self._try_trigger_mutation(context)
            if new_mutation:
                debug_log(f"[DEBUG MUTATION] ✓ Activated: {new_mutation.name}")
                self._activate_mutation(new_mutation)
            else:
                debug_log(f"[DEBUG MUTATION] Random check failed")
        else:
            debug_log(f"[DEBUG MUTATION] Skipping (cooldown: {self.cooldown})")
        
        # Check for combos
        self._check_combos()
        
        # Return only mutations that are actually active (not fading/expired)
        active = [m for m, turns, state in self.active_mutations if turns > 0]
        debug_log(f"[DEBUG MUTATION] Returning {len(active)} active mutations: {[m.name for m in active]}")
        debug_log(f"[DEBUG MUTATION] Total tracked (including fading): {len(self.active_mutations)}")
        return active
    
    def _update_active_mutations(self):
        """Update durations and states of active mutations."""
        from engine.debug import debug_log
        
        updated = []
        
        for mutation, turns_remaining, state in self.active_mutations:
            debug_log(f"[DEBUG MUTATION] Updating {mutation.name}: {turns_remaining} turns left, state={state}")
            
            if turns_remaining > 0:
                # Decrement duration
                new_turns = turns_remaining - 1
                
                # Update state
                if new_turns == 0:
                    new_state = MutationState.FADING
                    debug_log(f"[DEBUG MUTATION] {mutation.name} is FADING (will expire next turn)")
                elif len(self.active_mutations) > 1:
                    new_state = MutationState.STACKING
                else:
                    new_state = MutationState.ACTIVE
                
                updated.append((mutation, new_turns, new_state))
            else:
                # Mutation has expired
                debug_log(f"[DEBUG MUTATION] {mutation.name} EXPIRED and removed")
        
        self.active_mutations = updated
        debug_log(f"[DEBUG MUTATION] After update: {len(updated)} mutations still active")
    
    def _try_trigger_mutation(self, context: Dict) -> Optional[Mutation]:
        """Try to trigger a new mutation based on context."""
        choice_count = context.get('choice_count', 0)
        revelation_level = context.get('revelation_level', 0)
        instability = context.get('instability_level', 0)
        
        # Escalating frequency based on game progress - MUCH HIGHER CHANCES
        if choice_count <= 3:
            # Very early game: 40% chance (was 10%), COMMON MODERATE only
            base_chance = 0.40
            pool = [m for m in self.MODERATE_MUTATIONS if m.rarity == MutationRarity.COMMON]
        elif choice_count <= 8:
            # Early game: 50% chance (was 20%), all MODERATE
            base_chance = 0.50
            pool = self.MODERATE_MUTATIONS.copy()
        elif choice_count <= 15:
            # Mid game: 60% chance (was 30%), MODERATE + UNCOMMON WILD
            base_chance = 0.60
            pool = self.MODERATE_MUTATIONS.copy()
            pool.extend([m for m in self.WILD_MUTATIONS if m.rarity in [MutationRarity.COMMON, MutationRarity.UNCOMMON]])
        elif choice_count <= 25:
            # Late game: 70% chance (was 40%), all MODERATE + WILD, RARE possible
            base_chance = 0.70
            pool = self.MODERATE_MUTATIONS.copy() + self.WILD_MUTATIONS.copy()
        else:
            # End game: 80% chance (was 50%), everything including ULTRA_RARE
            base_chance = 0.80
            pool = self.MODERATE_MUTATIONS.copy() + self.WILD_MUTATIONS.copy()
        
        from engine.debug import debug_log
        
        # Adjust by instability
        final_chance = base_chance + (instability * 0.05)
        
        debug_log(f"[DEBUG MUTATION] Base chance: {base_chance*100}%, Final chance: {final_chance*100}%, Pool size: {len(pool)}")
        
        roll = random.random()
        debug_log(f"[DEBUG MUTATION] Rolled: {roll:.2f} vs {final_chance:.2f}")
        
        if roll < final_chance:
            debug_log(f"[DEBUG MUTATION] Success! Selecting mutation from pool...")
            return self._select_mutation(pool, context)
        
        debug_log(f"[DEBUG MUTATION] Failed roll")
        return None
    
    def _select_mutation(self, pool: List[Mutation], context: Dict) -> Mutation:
        """Select a mutation from pool based on rarity."""
        # Filter out recently used
        available = [m for m in pool if m.key not in self.mutation_history[-5:]]
        if not available:
            available = pool
        
        # Filter out non-stackable if we have active mutations
        if self.active_mutations:
            available = [m for m in available if m.can_stack]
        
        if not available:
            available = pool
        
        # Weight by rarity
        weights = []
        for m in available:
            if m.rarity == MutationRarity.COMMON:
                weights.append(60)
            elif m.rarity == MutationRarity.UNCOMMON:
                weights.append(30)
            elif m.rarity == MutationRarity.RARE:
                weights.append(8)
            else:  # ULTRA_RARE
                weights.append(2)
        
        chosen = random.choices(available, weights=weights)[0]
        self.mutation_history.append(chosen.key)
        
        return chosen
    
    def _force_mutation(self, context: Dict) -> Mutation:
        """Force a mutation to occur (for guaranteed turns)."""
        choice_count = context.get('choice_count', 0)
        
        # Select appropriate pool based on progress
        if choice_count <= 3:
            pool = [m for m in self.MODERATE_MUTATIONS if m.rarity == MutationRarity.COMMON]
        elif choice_count <= 8:
            pool = self.MODERATE_MUTATIONS.copy()
        else:
            pool = self.MODERATE_MUTATIONS.copy() + self.WILD_MUTATIONS.copy()
        
        return self._select_mutation(pool, context)
    
    def _activate_mutation(self, mutation: Mutation):
        """Activate a new mutation."""
        state = MutationState.ACTIVATING if mutation.duration > 0 else MutationState.ACTIVE
        self.active_mutations.append((mutation, mutation.duration, state))
        
        # MUCH shorter cooldowns
        if mutation.rarity in [MutationRarity.RARE, MutationRarity.ULTRA_RARE]:
            self.cooldown = random.randint(1, 2)  # Was 4-6
        else:
            self.cooldown = 0  # Was 2-4, now NO COOLDOWN for common!
    
    def _check_combos(self):
        """Check for mutation combos."""
        if len(self.active_mutations) < 2:
            self.combo_active = None
            return
        
        keys = [m.key for m, _, _ in self.active_mutations]
        
        # Define combos
        if 'open_dialogue' in keys and 'fourth_wall' in keys:
            self.combo_active = "meta_conversation"
        elif 'time_pressure' in keys and 'choice_inflation' in keys:
            self.combo_active = "overwhelming_chaos"
        elif 'format_shift' in keys and 'narrator_split' in keys:
            self.combo_active = "competing_formats"
        elif 'debug_mode' in keys and 'code_editor' in keys:
            self.combo_active = "system_access"
        else:
            self.combo_active = None
    
    def get_active_mutations_summary(self) -> str:
        """Get summary of active mutations for AI context."""
        if not self.active_mutations:
            return ""
        
        lines = ["ACTIVE MUTATIONS:"]
        for mutation, turns_left, state in self.active_mutations:
            lines.append(f"- {mutation.name} ({state.value}, {turns_left} turns left)")
            lines.append(f"  Trigger: {mutation.narrative_trigger}")
            if mutation.requires_special_input:
                lines.append(f"  REQUIRES SPECIAL INPUT MODE")
        
        if self.combo_active:
            lines.append(f"\nCOMBO ACTIVE: {self.combo_active}")
        
        return "\n".join(lines)
    
    def get_state_dict(self) -> Dict:
        """Get mutation state for saving."""
        return {
            'mutation_history': self.mutation_history,
            'cooldown': self.cooldown,
        }
    
    def load_state(self, state: Dict):
        """Load mutation state from save."""
        self.mutation_history = state.get('mutation_history', [])
        self.cooldown = state.get('cooldown', 0)

