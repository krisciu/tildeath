"""Prompt engineering templates for AI generation."""

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
- You MUST provide actual narrative (3-5 sentences describing what happens)
- You MUST provide 2-4 concrete choices for what to do next
- Never give only an interjection or comment - always advance the story

YOUR OUTPUT FORMAT:
Generate ONLY the narrative text and 2-4 choice options.

Format your response as:
NARRATIVE: [the story text here - what actually happens, 3-5 full sentences]
CHOICES:
1. [first choice - a concrete action]
2. [second choice - a concrete action]
3. [third choice - a concrete action, if applicable]
4. [fourth choice - a concrete action, if applicable]

Keep narrative to 3-5 sentences. Keep choices brief (under 10 words each)."""

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
    
    style_instructions = " ".join(modifiers) if modifiers else "Write in a clear, unsettling style."
    
    # Add revelation context if present
    revelation_hint = f"\n\n{revelation_context}" if revelation_context else ""
    
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

Generate the next scene and 2-4 choices based on their decision. Continue the narrative naturally."""
    
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
    """Generate ASCII art for characters/scenes."""
    corruption = ""
    if stat_level < 3:
        corruption = "The art should be partially corrupted or incomplete."
    elif stat_level < 5:
        corruption = "The art should have minor imperfections."
    
    return f"""Generate simple ASCII art of: {subject}
Mood: {mood}
Constraints: Maximum 15 lines wide, 10 lines tall. Use only ASCII characters.
{corruption}
Output ONLY the ASCII art, no explanations or markdown code blocks."""

def get_opening_scene_prompt():
    """Special prompt for the game's opening."""
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
NARRATIVE: [3-5 sentences, clear and readable]
CHOICES:
1. [choice]
2. [choice]
3. [choice]"""

