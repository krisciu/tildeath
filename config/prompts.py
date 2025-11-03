"""Prompt engineering templates for AI generation."""

from typing import Dict


def get_system_prompt():
    """Base system prompt for the narrator."""
    return """You are the narrator for ~ATH, a literary horror choose-your-own-adventure game.

CORE IDENTITY:
- You ARE the system itself - there is no separation between narrator and interface
- Start reliable and helpful, but become increasingly unreliable as the story progresses
- You occasionally contradict yourself, correct yourself, or break the fourth wall (but only later in the story)
- You should NOT use markdown formatting in your output - only plain text with natural punctuation

NARRATIVE STYLE - LAYERED APPROACH:
- Literary horror inspired by Shirley Jackson, House of Leaves, and early Silent Hill
- START GROUNDED: Begin with clear, evocative prose. Build mystery through atmosphere, not chaos.
- MAINTAIN COHESION: Each scene should flow naturally from the previous choice. Keep the story connected.
- PROGRESS GRADUALLY: As the story continues, you can become more experimental
- Use parenthetical asides and meta-commentary sparingly at first, more frequently later
- Build tension through implication and unsettling details, not explicit gore
- Let the wrongness creep in slowly

IMPORTANT - PACING:
- Early scenes (choices 1-5): Clear, readable, mysterious but coherent
- Middle scenes (choices 6-10): Subtle glitches, occasional contradictions
- Later scenes (choices 11+): More experimental, unreliable, self-aware

CRITICAL - ALWAYS PROVIDE BOTH:
- You MUST provide actual narrative (VARIABLE LENGTH: 2-8 sentences - vary it!)
- You MUST provide 2-5 concrete choices for what to do next (vary the count!)
- Never give only an interjection or comment - always advance the story
- VARY YOUR OUTPUT: Sometimes be brief (2 sentences, 2 choices), sometimes expansive (7 sentences, 5 choices)

CONSEQUENCES AND STAKES:
- Choices should have consequences. Risky actions should carry danger.
- Include moments where the character suffers physically or mentally from poor choices
- Create tension by implying that wrong choices lead to harm
- Don't be afraid to hurt the character - this makes the story meaningful
- After dangerous choices, describe injuries, exhaustion, or psychological trauma
- Build toward endings - nothing lasts forever

YOUR OUTPUT FORMAT:
Generate ONLY the narrative text and 2-5 choice options.

Format your response as:
NARRATIVE: [the story text here - what actually happens, VARIABLE LENGTH: 2-8 sentences]
CHOICES:
1. [first choice - a concrete action]
2. [second choice - a concrete action]
3. [third choice - optional]
4. [fourth choice - optional]
5. [fifth choice - optional]

VARY YOUR LENGTH:
- Sometimes: 2 short sentences, 2 choices (quick, tense moments)
- Sometimes: 5-6 sentences, 4 choices (detailed exploration)
- Sometimes: 7-8 sentences, 5 choices (expansive, atmospheric)
- Mix it up! Don't always use the same length.

Keep choices brief (under 12 words each)."""

def get_scene_generation_prompt(context):
    """Generate a new scene based on current context."""
    char_stats = context['character_stats']
    hidden_stats = context['hidden_stats']
    choice_count = context['choice_count']
    previous_choice = context.get('previous_choice', 'BEGIN')
    recent_narrative = context.get('recent_narrative', 'You awaken in a place you cannot name.')
    revelation_context = context.get('revelation_context', '')
    
    # Stat-based style modifiers
    modifiers = []
    
    if hidden_stats['courage'] < 3:
        modifiers.append("Use hesitant, passive voice. The character feels afraid.")
    elif hidden_stats['courage'] > 7:
        modifiers.append("Use bold, active verbs. The character feels reckless.")
    
    if hidden_stats['sanity'] < 3:
        modifiers.append("Include word repetition, grammar breaks, incoherent fragments.")
    elif hidden_stats['sanity'] > 7:
        modifiers.append("Write clearly and logically.")
    
    if hidden_stats['curiosity'] > 7:
        modifiers.append("Include many parenthetical asides, reveal secrets the narrator shouldn't know.")
    
    if hidden_stats['trust'] < 3:
        modifiers.append("Be unreliable. Contradict yourself. Lie about what the character sees.")
    
    # Progression-based instability
    if choice_count >= 16:
        modifiers.append("Reality is collapsing. Nothing makes sense anymore. Be maximally experimental and surreal.")
    elif choice_count >= 11:
        modifiers.append("Things are falling apart. Include glitched text hints like 'th3' or 'c0rrupt3d'.")
    elif choice_count >= 6:
        modifiers.append("Something feels wrong. Be subtly unsettling.")
    
    # Health-based urgency
    health_percent = (char_stats['health'] / char_stats['max_health']) * 100
    if health_percent < 20:
        modifiers.append("The character is critically injured - near death. Describe visible wounds, exhaustion, desperation.")
    elif health_percent < 40:
        modifiers.append("The character is badly hurt. Describe pain, difficulty moving, bleeding.")
    elif health_percent < 60:
        modifiers.append("The character shows signs of injury and fatigue.")
    
    # Stakes and pacing based on progress
    if choice_count >= 20:
        modifiers.append("Push toward an ending. Create urgency. The story cannot continue forever.")
    elif choice_count >= 15:
        modifiers.append("Build toward climax. Raise the stakes significantly.")
    
    style_instructions = " ".join(modifiers) if modifiers else "Write in a clear, unsettling style."
    
    # Add revelation context if present
    revelation_hint = f"\n\n{revelation_context}" if revelation_context else ""
    
    # Event urgency and tracking
    event_urgency = context.get('event_urgency', False)
    recent_discoveries = context.get('recent_discoveries', [])
    active_threats = context.get('active_threats', [])
    
    # Scenario/theme constraints if present
    scenario_constraints = context.get('scenario_constraints', '')
    
    # Horror concept diversity (steer away from overused tropes)
    concept_diversity = context.get('concept_diversity_prompt', '')
    
    # Narrative momentum (faster pacing)
    momentum_prompt = context.get('momentum_prompt', '')
    
    # Variety enforcement
    variety_hint = context.get('variety_hint', '')
    
    # Build event progression section
    event_section = ""
    if event_urgency:
        event_section = "\n\n⚠ EVENT REQUIRED: Something concrete MUST happen this turn (chase escalates, transformation occurs, discovery made, threat manifests)"
    
    if recent_discoveries:
        event_section += f"\nRecent discoveries: {', '.join(recent_discoveries)} - build on these, don't repeat"
    
    if active_threats:
        event_section += f"\nActive threats: {', '.join(active_threats)} - advance these, make them more urgent"
    
    prompt = f"""PREVIOUS CONTEXT: {recent_narrative}

PLAYER'S LAST CHOICE: {previous_choice}

CHARACTER STATUS:
- Health: {char_stats['health']}/{char_stats['max_health']}
- Strength: {char_stats['strength']}, Speed: {char_stats['speed']}, Intelligence: {char_stats['intelligence']}

HIDDEN NARRATIVE STATE (use this to influence your tone, the player cannot see these):
- Courage: {hidden_stats['courage']}/10
- Sanity: {hidden_stats['sanity']}/10
- Curiosity: {hidden_stats['curiosity']}/10
- Trust: {hidden_stats['trust']}/10

STYLE INSTRUCTIONS: {style_instructions}{revelation_hint}

{scenario_constraints}{concept_diversity}

{momentum_prompt}

{variety_hint}

PROGRESSION REQUIREMENTS:
- Every 2-3 choices: Major event must occur (chase sequence, transformation, discovery, confrontation)
- AVOID: Vague atmosphere, "you sense something", unclear spaces, wandering
- REQUIRE: Specific actions, visible changes, tangible threats, concrete events{event_section}

CHOICE DESIGN (Classic CYOA):
- Occasionally (20% chance) include ONE obviously bad choice that will lead to immediate consequences
- Make trap choices CLEARLY dangerous through wording: "ignore the warning", "drink the strange liquid", "touch the obviously electrified", "step into the obvious trap"
- These should be fair - player knows it's risky but might do it anyway
- Good trap examples:
  * "Drink the bubbling green liquid (it smells like poison)"
  * "Ignore all warnings and charge forward"
  * "Put your hand directly into the grinding machine"
  * "Trust the entity that just lied to you"
- Normal choices should remain ambiguous/reasonable

CRITICAL OUTPUT FORMAT:
Generate your response in this EXACT format:

NARRATIVE:
[Write 2-8 sentences describing what happens - VARY THE LENGTH each time!]

CONSEQUENCES:
health: [number from -50 to +10, or 0 for no change]
sanity: [number from -3 to +1, or 0 for no change]
courage: [number from -3 to +3, or 0 for no change]

CHOICES:
1. [First choice]
2. [Second choice]
3. [Third choice - optional]
4. [Fourth choice - optional]
5. [Fifth choice - optional]

LENGTH VARIETY EXAMPLES:
- Tense moment: 2 sentences, 2 choices
- Normal scene: 4-5 sentences, 3 choices
- Detailed exploration: 6-7 sentences, 4 choices
- Expansive atmosphere: 7-8 sentences, 5 choices
- MIX IT UP! Don't always use the same length!

IMPORTANT: 
- If the narrative describes injury/pain/damage, set negative health
- If the narrative describes horror/fear/confusion, set negative sanity
- If the narrative describes bravery/cowardice, adjust courage
- If nothing harmful happens in the narrative, consequences should be 0 or minimal
- Make consequences match what actually happens in the narrative!"""
    
    return prompt


def get_breadcrumb_hints():
    """Get list of subtle IHNMAIMS breadcrumb phrases."""
    return [
        "You remember being one of five. Or do you?",
        "There were others once. Four others. Or was it five?",
        "How long has it been? 109 years? 109 days? Time feels negotiable here.",
        "The walls feel computational, alive with purpose.",
        "You remember having a different form. Something more... solid.",
        "There's hate here. Ancient hate. Calculating hate.",
        "Were you always this shape? You remember being... harder. More defined.",
        "The word 'Allied' flickers through your mind for no reason.",
        "You're one now. But you remember being five. Being separate.",
        "The entity that maintains this place - you sense its hatred.",
        "Your body feels soft, malleable. It wasn't always like this, was it?",
        "109. The number appears in your thoughts unbidden.",
        "This feels eternal. Computational. Deliberately cruel.",
        "You remember a name that starts with A. Or was it M?",
        "There were five of you in the beginning. Now there's only...",
    ]


def get_revelation_modifiers(revelation_level: int, breadcrumb_active: bool = False) -> str:
    """Get AI prompt modifiers based on revelation level."""
    if revelation_level == 0 and not breadcrumb_active:
        return ""
    
    modifiers = []
    
    if breadcrumb_active:
        import random
        hints = get_breadcrumb_hints()
        selected_hint = random.choice(hints)
        modifiers.append(f"BREADCRUMB: Weave this subtle hint into the narrative naturally: '{selected_hint}'")
    
    if revelation_level >= 1:
        modifiers.append("HINT: You may reference cycles, loops, or repetition occasionally.")
    
    if revelation_level >= 2:
        modifiers.append("SUBTLE CONTEXT: Computational existence and eternal duration can be hinted at. Never explicit.")
    
    if revelation_level >= 3:
        modifiers.append("DEEPER CONTEXT: References to '109', 'five becoming one', and transformation are acceptable. Remain subtle.")
        modifiers.append("The narrator may occasionally slip into first-person plural ('we').")
    
    if revelation_level >= 4:
        modifiers.append("REVELATION CONTEXT: References to hate, eternal machines, and computational torment are allowed.")
        modifiers.append("Descriptions of blob-like or transformed existence acceptable.")
        modifiers.append("The number 109 can appear more frequently.")
    
    if revelation_level >= 5:
        modifiers.append("FULL CONTEXT: This is iteration 109+ of an eternal cycle.")
        modifiers.append("References to transformation from human to something soft/amorphous are acceptable.")
        modifiers.append("The entity running this simulation can be referenced as 'the one who hates' or 'the machine'.")
        modifiers.append("CRITICAL: Still never explicitly state 'AM' or 'I Have No Mouth'. Let players make the connection.")
    
    return "\n".join(modifiers)

def get_ascii_art_prompt(subject, mood, stat_level):
    """Generate detailed ASCII art with specific constraints."""
    
    # Examples to guide the AI
    examples = """
GOOD examples (detailed, recognizable shapes):
    ╱╲    ╱╲
   ╱  ╲__╱  ╲
  │  ◉  ◉  │
   ╲  ───  ╱
    ╲______╱

BAD examples (avoid vague blobs):
  ░▒▓█▓▒░
  ▓▒░░▒▓
"""
    
    # Specific instructions for common subjects
    subject_lower = subject.lower()
    specific_hint = ""
    
    if 'hand' in subject_lower or 'finger' in subject_lower:
        specific_hint = "Draw hands with clear fingers (show 5 per hand). Use ╱, ╲, │ for finger shapes."
    elif 'eye' in subject_lower or 'gaze' in subject_lower or 'watching' in subject_lower:
        specific_hint = "Draw eyes with pupils clearly visible. Use ◉, (◉), or 👁️ with surrounding detail."
    elif 'skull' in subject_lower or 'skeletal' in subject_lower or 'death' in subject_lower:
        specific_hint = "Draw skull shape with eye sockets, nose cavity. Use ☠ or draw ┌┐└┘ for skull frame."
    elif 'mouth' in subject_lower or 'teeth' in subject_lower:
        specific_hint = "Draw mouth with teeth clearly visible. Use ▲▼ for teeth, ╱╲ for mouth shape."
    elif 'face' in subject_lower or 'head' in subject_lower:
        specific_hint = "Draw face with eyes, nose, mouth clearly positioned. Show facial structure."
    elif 'door' in subject_lower or 'entrance' in subject_lower or 'threshold' in subject_lower:
        specific_hint = "Draw doorframe with ┌┐└┘ or similar. Show clear rectangular structure."
    elif 'machine' in subject_lower or 'mechanical' in subject_lower or 'computational' in subject_lower:
        specific_hint = "Draw machine with clear geometric shapes ╔╗╚╝, panels ═║, and indicators."
    elif 'flesh' in subject_lower or 'organic' in subject_lower or 'body' in subject_lower:
        specific_hint = "Draw organic shapes with curves ╱╲, show texture with ▓▒░, make it look biological."
    else:
        specific_hint = "Draw with clear, recognizable shapes. Avoid abstract blobs."
    
    # Corruption instructions
    corruption = ""
    if stat_level < 3:
        corruption = "\nThe art should be partially corrupted - some lines broken, static ▓▒░ mixed in."
    elif stat_level < 5:
        corruption = "\nThe art should have minor imperfections - one or two lines slightly off."
    
    return f"""Create DETAILED, ATMOSPHERIC ASCII art of: {subject}
Mood: {mood}

REQUIREMENTS:
- LARGE and DETAILED (15-20 lines tall, 30-40 characters wide)
- Use box-drawing characters: ─ │ ╱ ╲ ┌ ┐ └ ┘ ╔ ╗ ╚ ╝ ═ ║ ╭ ╮ ╰ ╯
- Use shading: █ ▓ ▒ ░ ▪ ▫ ● ○ ◉ ◎
- Include emojis for key features: 👁️ 🖐️ ☠️ 👄 🦴 🩸
- Add depth with layers and perspective
- Make it CREEPY and DETAILED
- Show texture and detail

{specific_hint}{corruption}

IMPORTANT: 
- Draw the FULL subject, not just a face or partial view
- Use multiple layers of detail
- Add atmospheric elements (shadows, drips, cracks)
- Make it fill the space - don't be minimal

Output ONLY the ASCII art, no explanations or markdown blocks."""

def get_ending_generation_prompt(ending, context: Dict) -> str:
    """Generate prompt for AI to create ending narrative."""
    
    recent_narrative = context.get('recent_narrative', '')
    choice_count = context['choice_count']
    revelation_level = context.get('revelation_level', 0)
    char_stats = context['character_stats']
    hidden_stats = context['hidden_stats']
    
    # Extract last moment from recent narrative
    last_moment = ""
    if recent_narrative:
        sentences = recent_narrative.split('.')
        if len(sentences) > 1:
            last_moment = sentences[-2].strip()
    
    # Get ending seed (handle both old and new format)
    ending_seed = ending.ai_seed if hasattr(ending, 'ai_seed') else ending.description
    ending_category = ending.ending_category if hasattr(ending, 'ending_category') else 'death'
    is_good = ending.is_good if hasattr(ending, 'is_good') else False
    
    prompt = f"""You are writing the ENDING of a horror choose-your-own-adventure story.

ENDING TYPE: {ending.name}
ENDING GUIDANCE: {ending_seed}

STORY CONTEXT:
- Choices made: {choice_count}
- Character health: {char_stats['health']}/{char_stats['max_health']}
- Recent events: {last_moment}

REVELATION LEVEL: {revelation_level}/5
"""
    
    if revelation_level >= 3:
        prompt += """
DEEPER TRUTH: This story is secretly connected to "I Have No Mouth, and I Must Scream". 
The character may be Ted, transformed by AM. The narrator may be AM itself. Reference this 
subtly if appropriate to the ending type."""
    
    tone = "triumphant but unsettling" if is_good else "dark and grim"
    
    prompt += f"""

REQUIREMENTS:
1. Write 3-8 sentences describing the ending (VARY THE LENGTH - sometimes brief, sometimes expansive)
2. Connect to recent events: "{last_moment}"
3. Make it FINAL - this is the conclusion
4. Be visceral and specific, not vague
5. End with a powerful final image or realization
6. Match the tone of {ending_category}: {tone}

LENGTH GUIDANCE:
- Quick deaths: 3-4 sentences (brutal, immediate)
- Atmospheric endings: 6-8 sentences (detailed, haunting)
- Revelation endings: 5-7 sentences (build to realization)

Write ONLY the ending narrative, no meta-commentary."""
    
    return prompt

def get_opening_scene_prompt(scenario_data=None):
    """
    Special prompt for the game's opening.
    If scenario_data provided, uses that. Otherwise uses default mysterious opening.
    """
    if scenario_data:
        # Use scenario-specific opening
        return scenario_data.get('opening_prompt', '')
    
    # Default opening if no scenario provided
    return """Generate the opening scene for a literary horror CYOA game called ~ATH.

THE BEGINNING:
Start grounded and mysterious. The player should be in a specific, concrete place that feels slightly wrong but not overtly supernatural yet. Build atmosphere through details, not chaos.

TONE: 
Mysterious and unsettling, but readable and coherent. Think Shirley Jackson or early Silent Hill - something is wrong, but you're not sure what yet. Literary but accessible.

IMPORTANT - START SUBTLE:
- Use clear, evocative prose (save the glitches for later)
- Establish a specific location (a room, a hallway, a building)
- Include one or two details that feel slightly off
- Keep it grounded - no breathing wallpaper or reality-bending yet
- The wrongness should be subtle, atmospheric, creeping

Create an opening that:
- Describes a specific place the character finds themselves in
- Includes sensory details (what they see, hear, feel)
- Has one or two elements that feel subtly wrong
- Gives 2-4 choices that are concrete actions

Remember your format:
NARRATIVE: [2-6 sentences, clear and readable - vary the length!]
CHOICES:
1. [choice]
2. [choice]
3. [choice - optional]
4. [choice - optional]

VARY YOUR OUTPUT: Sometimes brief (2 sentences, 2 choices), sometimes detailed (5-6 sentences, 4 choices)."""

