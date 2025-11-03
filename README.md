# 🌀 ~ATH (TILDEATH)

> A haunted terminal that tells stories which only exist while you're reading them.

## What is this?

An experimental text-based horror game that lives in your terminal. It's a Choose Your Own Adventure story, but:

- **Every playthrough is unique** - AI generates the entire narrative dynamically
- **The narrator is unreliable** - It lies, contradicts itself, and sometimes breaks the fourth wall
- **Typography becomes storytelling** - Text decays, spirals, shatters (House of Leaves meets terminal aesthetics)
- **Nothing is saved** - Stories exist only during your session... except for ghost memories that shouldn't persist, but do

## Features

- 🤖 **AI-Driven Narrative** - Powered by Claude API for unique, literary horror prose
- 📊 **Dual Stat System** - Visible character stats (HP, STR, SPD, INT) + hidden narrative stats (courage, sanity, curiosity, trust)
- 🎨 **Experimental Typography** - Glitching text, scattered words, spiraling effects
- 👻 **Ghost Memory** - The program remembers your previous sessions cryptically
- 🎭 **Unreliable Narrator** - A single voice that shifts between helpful, gaslighting, and confused
- 🌀 **Progressive Instability** - The longer you play, the more reality breaks down

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/krisciu/tildeath/main/install.sh | bash
```

## Setup API Key

Get a key at: https://console.anthropic.com/

Then set it:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Or create `~/.ATH/.env`:
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > ~/.ATH/.env
```

## Run

```bash
tildeath
```

## How It Works

### The Story Engine

The game doesn't have pre-written content. Instead:

1. You start in a randomly generated opening scene
2. Every choice you make modifies hidden stats
3. These stats influence the AI's writing style and the narrator's behavior
4. Visual effects intensify as you progress
5. The session ends when you die, lose sanity, or exhaust the narrative

### Hidden Stats

All stats are hidden from the player - you never see numbers, only experience their effects through the narrative.

Your choices secretly modify stats that influence the story:

- **Character Stats** (health, strength, speed, intelligence) - Affect what actions are possible
- **Narrative Stats** (courage, sanity, curiosity, trust) - Shape the narrator's voice and reliability

These stats guide the AI's writing style, but you never see them directly. You only feel their effects.

### Progression System

Visual effects and instability increase based on:

- **Choice count** - Every 5 choices = threshold increase
- **Stat thresholds** - Low sanity/trust = more glitches
- **Critical events** - Deaths, discoveries, reality breaks

Choices 1-5: Clean, subtle
Choices 6-10: Minor glitches
Choices 11-15: Major disruptions
Choices 16+: Reality collapse

### Typography Effects

The game uses various experimental text effects:

- **Glitching** - Character substitution (e→3, a→@)
- **Spacing** - W o r d s  s t r e t c h  a p a r t
- **Repetition** - Words repeat repeat
- **Corruption** - U̷n̴i̶c̸o̷d̸e̴ ̶d̸e̷c̸a̷y̴
- **Strikethrough** - ~~safe~~ trapped
- **Marginalia** - [notes that shouldn't exist]
- **Spiraling** - Text spirals inward during paranoia
- **Scattering** - Words scattered across screen during panic

## Inspirations

- **House of Leaves** (Mark Z. Danielewski) - Experimental typography and unreliable narration
- **Lemony Snicket** (Daniel Handler) - Self-aware narrator and visual storytelling
- **The Stanley Parable** - Meta-narrative and narrator relationship
- **Control** (Remedy Entertainment) - Reality distortion and bureaucratic horror
- **Harlan Ellison** - Thematic resonance with computational horror and eternal cycles

## Technical Details

### Architecture

```
-ATH/
├── main.py                # Entry point & game loop
├── engine/
│   ├── story_engine.py    # State management & stats
│   ├── ai_adapter.py      # Claude API integration
│   ├── narrator.py        # Unreliable narrator system
│   ├── renderer.py        # Rich-based terminal UI
│   ├── typography.py      # Visual effects engine
│   └── session.py         # Ghost memory persistence
└── config/
    ├── prompts.py         # AI prompt templates
    └── settings.py        # Game configuration
```

### API Costs

Each playthrough makes roughly 10-30 API calls depending on length. Using Claude Sonnet, expect:

- Short session (5-10 choices): ~$0.05-0.10
- Medium session (10-20 choices): ~$0.10-0.20
- Long session (20+ choices): ~$0.20+

The game caches conversation history to maintain narrative consistency.

## Customization

### Change AI Model

Edit `.env`:
```
MODEL_NAME=claude-3-5-sonnet-20241022
```

### Adjust Progression

Edit `config/settings.py`:
```python
PROGRESSION_CONFIG = {
    "instability_choice_threshold": 5,  # Choices per threshold
    "minor_breakdown_at": 6,
    "major_breakdown_at": 11,
    "reality_collapse_at": 16,
}
```

### Modify Stats

Edit default stats in `config/settings.py`:
```python
DEFAULT_CHARACTER_STATS = {...}
DEFAULT_HIDDEN_STATS = {...}
```

## Known Quirks

- **The narrator lies** - Sometimes the story contradicts itself. This is intentional.
- **API errors become narrative** - If Claude times out, it becomes part of the glitch aesthetic
- **Ghost memory persists** - The `.ghost_memory` file stores fragments between sessions
- **No saving** - Each session is ephemeral (except ghost memories)
- **Terminal size matters** - Works best with at least 80 columns width

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Create a `.env` file with your API key.

### Text looks broken
Make sure your terminal supports Unicode and has a wide enough window (80+ columns).

### API errors
Check your API key and ensure you have credits in your Anthropic account.

### Game is too slow
Reduce `typing_speed` in `engine/renderer.py` or comment out typing effects.

## Future Expansions

- [ ] Multiple AI providers (OpenAI, Grok)
- [ ] ASCII art generation for scenes
- [ ] Session transcript export
- [ ] Multiple ending types
- [ ] Sound effects (terminal beeps)
- [ ] More sophisticated visual effects

## License

This is an experimental art project. Use and modify as you wish.

## Credits

Built for [Your Hackathon/Event]

Powered by:
- Claude (Anthropic) for AI generation
- Rich library for terminal UI
- House of Leaves for visual inspiration

---

> The best stories are the ones that know they're being told.
> Let the terminal speak back.

---

**Start the story:**
```bash
tildeath
```

(There is no back. Only forward. Until the end.)

